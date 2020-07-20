

def generator_function(apiname: str, data: dict):
    """
    根据接口名和传参data自动生成函数
    @param apiname: 接口名
    @param data: 传参data
    @return:
    """
    # 生成函数名：function_name
    function_name_list = []
    for index in range(len(apiname)):
        if apiname[index].islower() == True:
            function_name_list.append(apiname[index])
        elif apiname[index].isupper() == True:
            function_name_list.append('_')
            function_name_list.append(apiname[index])
        else:
            pass

    if function_name_list[0] == '_':
        function_name_list.pop(0)

    function_name_upper = ''.join(function_name_list)
    function_name = function_name_upper.lower()

    # 生成函数参数部分str：parameter
    parameter = str(data)
    parameter = parameter.replace("'", '')
    parameter = parameter.replace(':', '=')
    parameter = parameter.strip('{}')
    parameter = 'self, ' + parameter

    # 生成data部分：databody
    jsondic = data
    jsonkey = list(jsondic.keys())
    for i in range(len(jsondic)):
        jsondic[jsonkey[i]] = jsonkey[i]

    jsonadd = str(jsondic)
    jsonadd = jsonadd.replace("'", '')
    jsonadd = jsonadd.replace(':', '=')
    jsonadd = jsonadd.strip('{}')
    databody = apiname + ',' + jsonadd

    # 生成函数
    print('def ' + function_name + '(' + parameter + '):')
    print('\t' + 'result = self.login.create_api' + '(' + databody + ')')
    print('\t' + 'res = result.json()')
    print('\t' + 'return res')


generator_function('AddCoop',
                   {"CoopShortName":"看我","CoopTagId":1022,"CoopFullName":"手工","Uscc":"河南省","BankName":"欧文九年","BankCardNum":"3256732487465746","CtctName":"手工","CtctMobile":"13698776534","IdCardNum":"320687319873419873","CooperationStatus":1,"RspsUserId":101,"BusinessLicenseUrl":"/dajiaying/web/supplierManager202006181727579621"})
