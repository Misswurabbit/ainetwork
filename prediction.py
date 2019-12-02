#encoding: utf-8

import pandas as pd
import time
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
import db.db as db
import redis
import sys

input_dim = 100
hidden_encoder_dim_1 = 133
hidden_encoder_dim_2 = 53
hidden_decoder_dim = 53
latent_dim = 33  # （latent Variable）
lam = 0

# 增量更新
add_ids = 500

# 阈值
ratio = 1.5
cpu_ratio = ratio
memory_ratio = ratio
disk_ratio = ratio
net_ratio = ratio


db_obj = db.database(dict=True)
r = redis.StrictRedis(host='127.0.0.1', port=6379, decode_responses=True)
r_key = 'ai_network_id'
nid = r.get('r_key') if r.get('r_key') else 0
nid = int(nid if int(nid) >= 100 else 100)
print("nid: "+str(nid))

# r.set(r_key,0)
# print(r.get(r_key))
# sys.exit(0)
def weight_variable(shape):
    # initial = tf.random_normal(shape)
    initial = tf.truncated_normal(shape, stddev=0.001)

    # 取正态分布的2σ部分
    return tf.Variable(initial)


def bias_variable(shape):
    initial = tf.constant(0., shape=shape)
    return tf.Variable(initial)


x = tf.placeholder("float", shape=[None, input_dim])  # input x [,784]
l2_loss = tf.constant(0.0)

# encoder1 W b
W_encoder_input_hidden_1 = weight_variable(
    [input_dim, hidden_encoder_dim_1])  # 784*1000
b_encoder_input_hidden_1 = bias_variable([hidden_encoder_dim_1])  # 1000
l2_loss += tf.nn.l2_loss(W_encoder_input_hidden_1)

# Hidden layer1 encoder
hidden_encoder_1 = tf.nn.relu(
    tf.matmul(x, W_encoder_input_hidden_1) + b_encoder_input_hidden_1)  # w*x+b

# encoder2 W b
W_encoder_input_hidden_2 = weight_variable(
    [hidden_encoder_dim_1, hidden_encoder_dim_2])  # 1000*400
b_encoder_input_hidden_2 = bias_variable([hidden_encoder_dim_2])  # 400
l2_loss += tf.nn.l2_loss(W_encoder_input_hidden_2)

# Hidden layer2 encoder
hidden_encoder_2 = tf.nn.relu(tf.matmul(
    hidden_encoder_1, W_encoder_input_hidden_2) + b_encoder_input_hidden_2)  # w*x+b

W_encoder_hidden_mu = weight_variable(
    [hidden_encoder_dim_2, latent_dim])  # 400*20
b_encoder_hidden_mu = bias_variable([latent_dim])  # 20
l2_loss += tf.nn.l2_loss(W_encoder_hidden_mu)

# Mu encoder=+
mu_encoder = tf.matmul(hidden_encoder_2, W_encoder_hidden_mu) + \
             b_encoder_hidden_mu  # mu_encoder:1*20(1*400 400*20)

W_encoder_hidden_logvar = weight_variable(
    [hidden_encoder_dim_2, latent_dim])  # W_encoder_hidden_logvar:400*20
b_encoder_hidden_logvar = bias_variable([latent_dim])  # 20
l2_loss += tf.nn.l2_loss(W_encoder_hidden_logvar)

# Sigma encoder
logvar_encoder = tf.matmul(hidden_encoder_2, W_encoder_hidden_logvar) + \
                 b_encoder_hidden_logvar  # logvar_encoder:1*20(1*400 400*20)

# Sample epsilon
epsilon = tf.random_normal(tf.shape(logvar_encoder), name='epsilon')

# Sample latent variable
std_encoder = tf.exp(0.5 * logvar_encoder)
# z_mu+epsilon*z_std=z,as decoder's input;z:1*20
z = mu_encoder + tf.multiply(std_encoder, epsilon)

W_decoder_z_hidden = weight_variable(
    [latent_dim, hidden_decoder_dim])  # W_decoder_z_hidden:20*400
b_decoder_z_hidden = bias_variable([hidden_decoder_dim])  # 400
l2_loss += tf.nn.l2_loss(W_decoder_z_hidden)

# Hidden layer decoder
# hidden_decoder:1*400(1*20 20*400)
hidden_decoder = tf.nn.relu(
    tf.matmul(z, W_decoder_z_hidden) + b_decoder_z_hidden)

W_decoder_hidden_reconstruction = weight_variable(
    [hidden_decoder_dim, input_dim])  # 400*784
b_decoder_hidden_reconstruction = bias_variable([input_dim])
l2_loss += tf.nn.l2_loss(W_decoder_hidden_reconstruction)

KLD = -0.5 * tf.reduce_sum(1 + logvar_encoder - tf.pow(mu_encoder, 2) -
                           tf.exp(logvar_encoder), reduction_indices=1)  # KLD

x_hat = tf.matmul(hidden_decoder, W_decoder_hidden_reconstruction) + \
        b_decoder_hidden_reconstruction  # x_hat:1*784(reconstruction x)

BCE = tf.reduce_sum(tf.nn.sigmoid_cross_entropy_with_logits(
    logits=x_hat, labels=x), reduction_indices=1)  # sum cross_entropy

loss = tf.reduce_mean(BCE + KLD)  # average value

regularized_loss = loss + lam * l2_loss

# Record the stored value of loss
loss_summ = tf.summary.scalar("lowerbound", loss)
train_step = tf.train.AdamOptimizer(0.001).minimize(
    regularized_loss)  # Optimization Strategy

# add op for merging summary
summary_op = tf.summary.merge_all()

# add Saver ops
saver = tf.train.Saver()

n_steps = int(1e5 + 1)  # step:1000000
batch_size = 100


def data_get_time(timestamp):
    input_data = time.localtime(timestamp)
    return time.strftime("%Y-%m-%d %H:%M:%S", input_data)

def prediction(input_data):
    # data = pd.read_csv("../data/machine_usage.csv", header=None,names=["machine_id", "time_stamp", "cpu_util_percent", "mem_util_percent", "mem_gps", "mkpi","net_in", "net_out", "disk_io_percent"], nrows=1000000)
    # data["time_stamp"] = data["time_stamp"].apply(data_get_time)
    # id = 'm_2043'
    # input_data = data[data['machine_id'] == id]
    # input_data.drop(['mem_gps', 'mkpi', 'net_in'], axis=1, inplace=True)

    data = np.array(input_data['cpu_util_percent']).reshape([-1, 1])

    flag = False
    output = []

    # cpu part
    with tf.Session() as sess:
        saver = tf.train.Saver()
        sess.run(tf.global_variables_initializer())
        scal = MinMaxScaler(feature_range=(0, 1))
        data = scal.fit_transform(data)
        saver.restore(sess, "./model/cpu/model_cpu.ckpt")
        feed_dict = {x: data.reshape([-1, 100])}
        result = sess.run([x_hat], feed_dict=feed_dict)[0]

        result = scal.fit_transform(result.reshape([-1, 1]))
        # result = result.reshape([-1, 100])
        diff = (data - result) + 1
        mean = np.mean(diff[89:99])
        if diff[99] > mean:
            ratio = diff[99] / mean
        else:
            ratio = mean / diff[99]
        if ratio > cpu_ratio:
            flag = True
            output.append('2')

    data = np.array(input_data['mem_util_percent']).reshape([-1, 1])
    # mem part
    with tf.Session() as sess:
        saver = tf.train.Saver()
        sess.run(tf.global_variables_initializer())
        scal = MinMaxScaler(feature_range=(0, 1))
        data = scal.fit_transform(data)
        saver.restore(sess, "./model/mem/model_mem.ckpt")
        feed_dict = {x: data.reshape([-1, 100])}
        result = sess.run([x_hat], feed_dict=feed_dict)[0]
        result = scal.fit_transform(result.reshape([-1, 1]))
        diff = (data - result) + 1
        mean = np.mean(diff[89:99])
        if diff[99] > mean:
            ratio = diff[99] / mean
        else:
            ratio = mean / diff[99]
        if ratio > memory_ratio:
            flag = True
            output.append('3')

    data = np.array(input_data['net_out']).reshape([-1, 1])
    # mem part
    with tf.Session() as sess:
        saver = tf.train.Saver()
        sess.run(tf.global_variables_initializer())
        scal = MinMaxScaler(feature_range=(0, 1))
        data = scal.fit_transform(data)
        saver.restore(sess, "./model/net/model_net.ckpt")
        feed_dict = {x: data.reshape([-1, 100])}
        result = sess.run([x_hat], feed_dict=feed_dict)[0]
        result = scal.fit_transform(result.reshape([-1, 1]))
        diff = (data - result) + 1
        mean = np.mean(diff[89:99])
        if diff[99] > mean:
            ratio = diff[99] / mean
        else:
            ratio = mean / diff[99]
        if ratio > net_ratio:
            flag = True
            output.append('1')

    data = np.array(input_data['disk_io_percent']).reshape([-1, 1])
    # mem part
    with tf.Session() as sess:
        saver = tf.train.Saver()
        sess.run(tf.global_variables_initializer())
        scal = MinMaxScaler(feature_range=(0, 1))
        data = scal.fit_transform(data)
        saver.restore(sess, "./model/io/model_io.ckpt")
        feed_dict = {x: data.reshape([-1, 100])}
        result = sess.run([x_hat], feed_dict=feed_dict)[0]
        result = scal.fit_transform(result.reshape([-1, 1]))
        diff = (data - result) + 1
        mean = np.mean(diff[89:99])
        if diff[99] > mean:
            ratio = diff[99] / mean
        else:
            ratio = mean / diff[99]
        if ratio > disk_ratio:
            flag = True
            output.append('4')

    output.sort()
    cur_id = r.get('r_key')
    print("cur_id: "+str(cur_id))
    if not output:
        out_str = '0'
        print('No anomoly')
    else:
        out_str = ','.join(output)
        print('Anomoly_type: '+out_str)
    sql = "update data set anomoly_type = '"+out_str+"' where id = "+str(int(cur_id)+100)
    result = db_obj.save(sql)
    if result is True:
        print("Save success:")
        r.set('r_key', str(int(cur_id)+1))
    else:
        print("Save error:")
    print('over')


def read_data_from_db(add_ids, nid):
    sql = "select * from data where anomoly_type = '-1' and id >= "+str(nid-100)+" limit "+str(100+add_ids)
    result = db_obj.fetch_all(sql)
    # print(result)
    return list(result)

def prediction_all(dataset):
    # print(len(dataset))
    for i in range(100, len(dataset)):
        # print(dataset.iloc[i-100:i])
        prediction(dataset.iloc[i-100:i])


data = read_data_from_db(add_ids, nid)
data = pd.DataFrame(data)
# print(data[:3])
# print(data)
# print(type(data))
prediction_all(data)
