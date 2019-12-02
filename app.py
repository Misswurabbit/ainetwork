# encoding: utf-8
from flask import Flask, request, jsonify, make_response, Blueprint
import json
import db.db as db
from flask_cors import CORS
import operator
from collections import OrderedDict

app = Flask(__name__)
CORS(app, supports_credentials=True)


def response_data(data):
    response = make_response(json.dumps(data))
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST,GET'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, X-Requested-With'
    return response


@app.route('/')
def index():
    # version 1.0
    # db_obj = db.database(dict=True)
    # sql = "select cpu_util_percent,disk_io_percent,machine_id,mem_util_percent,net_in,time_stamp,status,if(anomoly_type = '-1',0,1) predict_status from data where id in (select max(id) from data group by machine_id)"
    # result = db_obj.fetch_all(sql)
    # cpu_warning = 0
    # mem_warning = 0
    # disk_warning = 0
    # network_warning = 0
    # cpu_set = set()
    # for x in result:
    #     if int(x['cpu_util_percent']) > 80:
    #         cpu_set.add(x['machine_id'])
    #         cpu_warning += 1
    #     if int(x['mem_util_percent']) > 80:
    #         mem_warning += 1
    #     if int(x['disk_io_percent']) > 40:
    #         disk_warning += 1
    #     # if float(x['net_in']) > 40:
    #     #     network_warning += 1
    #     x['loc'] = '--'
    #
    # def by_name(t):
    #     return(t['cpu_util_percent'])
    # sorted_result = sorted(result, key=by_name, reverse=True)
    # return jsonify({'data': result, 'warning_data': sorted_result,'cpu_warning': len(cpu_set), 'mem_warning': mem_warning, 'disk_warning': disk_warning, 'network_warning': network_warning})

    # version 2.0
    # all machine list
    machine_id_list = ['m_1932', 'm_1933', 'm_1934', 'm_1935', 'm_1936', 'm_1937', 'm_1938', 'm_1940', 'm_1941',
                       'm_1942']
    # read cnt
    db_obj = db.database(dict=True)
    sql = "select max(id) mid from cnt"
    res = db_obj.fetch_all(sql)
    cnt = res[0]['mid']
    print(cnt)

    # init warning number
    cpu_warning = 0
    mem_warning = 0
    disk_warning = 0
    network_warning = 0
    cpu_set = set()

    # init data list
    data = []
    warning_data = []

    for id in range(len(machine_id_list)):
        # 读取某一台机器上的cnt那一行的数据
        sql = "select cpu_util_percent,disk_io_percent,machine_id,mem_util_percent,net_in,time_stamp,status,if(anomoly_type = '-1',0,1) predict_status from data where machine_id='" + str(
            machine_id_list[id]) + "' limit " + str(cnt) + ", 1"
        result = db_obj.fetch_all(sql)
        result = result[0]

        # 读取这台机器的预测状态缓存，即之前是否有预测错误
        sql = "select now_status,predict_status from status where machine_id='" + str(machine_id_list[id]) + "'"
        re = db_obj.fetch_all(sql)
        re = re[0]
        re_now_stuts = re['now_status']
        re_pre_status = re['predict_status']

        # 用阈值判断是否有异常的状态
        if int(result['cpu_util_percent']) > 30:
            cpu_set.add(result['machine_id'])
            cpu_warning += 1
        if int(result['mem_util_percent']) > 80:
            mem_warning += 1
        if int(result['disk_io_percent']) > 10:
            disk_warning += 1
            # if float(x['net_in']) > 40:
            #     network_warning += 1
        result['loc'] = '--'
        # 返回cnt时刻的机器的状态信息
        data.append(result)

        # 更新预测故障缓存
        if result['predict_status'] == 1:
            re_pre_status = re_pre_status + 1
            sql = "update status set predict_status = " + str(re_pre_status) + " where machine_id='" + str(
                machine_id_list[id]) + "'"
            r = db_obj.save(sql)

        # 更新报警机器列表
        if re_pre_status != 0:
            result['predict_status'] = 1
            warning_data.append(result)
    # 更新cnt时刻并返回保存
    cnt = cnt + 1
    sql = "update cnt set id = " + str(cnt)
    r = db_obj.save(sql)

    #返回结果
    return jsonify(
        {'data': data, 'warning_data': warning_data, 'cpu_warning': len(cpu_set), 'mem_warning': mem_warning,
         'disk_warning': disk_warning, 'network_warning': network_warning})


@app.route('/detail/<machine_id>', methods=["GET"])
def detail(machine_id):
    if not machine_id:
        return jsonify({'errormsg': 'params error!'})
    db_obj = db.database(dict=True)
    sql = "select max(id) mid from cnt"
    res = db_obj.fetch_all(sql)
    cnt = res[0]['mid']
    # print(cnt)
    sql = "select cpu_util_percent,disk_io_percent,machine_id,mem_util_percent,net_in,time_stamp,status,if(anomoly_type = '-1',0,1) predict_status from data where machine_id='" + str(
        machine_id) + "' limit 0," + str(cnt)
    result = db_obj.fetch_all(sql)
    # cnt = cnt + 1
    # print(cnt)
    # sql = "update cnt set id = " + str(cnt)
    # r = db_obj.save(sql)
    return jsonify({'data': result})


@app.route('/monitor/<machine_id>', methods=["GET", "POST"])
def monitor(machine_id):
    if not machine_id:
        return jsonify({'errormsg': 'params error!'})
    anomoly_type = {'1': 'net', '2': 'cpu', '3': 'memory', '4': 'disk'}
    db_obj = db.database(dict=True)
    sql = "select net_in,cpu_util_percent,mem_util_percent,disk_io_percent,anomoly_type,time_stamp from data where anomoly_type != '-1' and machine_id='" + str(
        machine_id) + "' limit 0,3"
    result = db_obj.fetch_all(sql)
    return_dict = {}
    net = []
    cpu = []
    memory = []
    disk = []
    for x in result:
        net.append([x['net_in'], x['time_stamp'], 1 if x['anomoly_type'].find('1') >= 0 else 0])
        cpu.append([x['cpu_util_percent'], x['time_stamp'], 1 if x['anomoly_type'].find('2') >= 0 else 0])
        memory.append([x['mem_util_percent'], x['time_stamp'], 1 if x['anomoly_type'].find('3') >= 0 else 0])
        disk.append([x['disk_io_percent'], x['time_stamp'], 1 if x['anomoly_type'].find('4') >= 0 else 0])
    return_dict['net'] = net
    return_dict['cpu'] = cpu
    return_dict['memory'] = memory
    return_dict['disk'] = disk
    return_dict['net_stat'] = {'Mean': 1, 'Std': 1, 'Maximum': 1, 'Minimum': 1}
    return_dict['cpu_stat'] = {'Mean': 1, 'Std': 1, 'Maximum': 1, 'Minimum': 1}
    return_dict['memory_stat'] = {'Mean': 1, 'Std': 1, 'Maximum': 1, 'Minimum': 1}
    return_dict['disk_stat'] = {'Mean': 1, 'Std': 1, 'Maximum': 1, 'Minimum': 1}
    return jsonify(return_dict)


@app.route('/warning/<machine_id>', methods=["GET"])
def warning(machine_id):
    # if not machine_id:
    #     return jsonify({'errormsg': 'params error!'})
    # db_obj = db.database(dict=True)
    # sql = "select anomoly_type,time_stamp from data where machine_id='" + str(
    #     machine_id) + "' and anomoly_type != '-1' limit 10"
    # result = db_obj.fetch_all(sql)
    # return_dict = {}
    # anomoly = []
    # anomoly_type = {'1': 'net', '2': 'cpu', '3': 'memory', '4': 'disk'}
    # for x in result:
    #     x['anomoly'] = [anomoly_type[str(y)] for y in x['anomoly_type'].split(',')]
    #
    # # del result['anomoly_type']
    # return jsonify({'data': result})

    if not machine_id:
        return jsonify({'errormsg': 'params error!'})
    db_obj = db.database(dict=True)
    sql = "select now_status,predict_status from status where machine_id='" + str(machine_id) + "'"
    re = db_obj.fetch_all(sql)
    re = re[0]
    re_now_stuts = re['now_status']
    re_pre_status = re['predict_status']
    sql = "select anomoly_type,time_stamp from anomoly where machine_id='" + str(
        machine_id) + "' limit 0," + str(re_pre_status)
    result = db_obj.fetch_all(sql)
    return_dict = {}
    anomoly = []
    anomoly_type = {'1': 'net', '2': 'cpu', '3': 'memory', '4': 'disk'}
    for x in result:
        x['anomoly'] = [anomoly_type[str(y)] for y in x['anomoly_type'].split(',')]

    # del result['anomoly_type']
    return jsonify({'data': result})


if __name__ == '__main__':
    app.run(debug=True, host='::', port=8080)
