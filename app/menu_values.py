import os
import sys



def values_from_dic(arr, d):
    """
    ToDo : The try catch block here is a bad fix. we do it only because during startup the loading time is too long and causes crash in nginx
    :param arr:
    :param d:
    :return:
    """

    global dictionaries

    df = dictionaries[d]
    ret = []
    try:
        for e in arr:
            if 'all' in e:
                ret.append("Все (" + str(e) + ")")
            else:
                if e in df:
                    ret.append(str(df[e]) + " (" + str(e) + ")")
                else:
                    ret.append(str("?????") + " (" + str(e) + ")")
    except Exception as ex:

        print("values_from_dic(arr, d): " + str(ex))

    return ret


def value_from_dic(d, v):
    """
    :param d:
    :param v:
    :return:
    """

    global dictionaries
    df = dictionaries[d]
    ret = []

    if 'all' in v:
        ret = str(v) + " (" + str(v) + ")"
    else:
        ret = str(df[v]) + " (" + str(v) + ")"

    return ret


def has_element_or_create(j, ele):
    if ele not in j:
        j[ele] = {}


j_menu = {}


def make_j_menu_values(j_menu):
    global menu_values

    # arr = menu_values["all_menu_values"]
    arr = [[0, 1 , 2 , 3 , 4, 5, 6]]
    # for index, row in df_menu.iterrows():
    for row in arr:
        has_element_or_create(j_menu, row[0])
        has_element_or_create(j_menu[row[0]], str(row[1]))
        has_element_or_create(j_menu[row[0]][str(row[1])], row[2])
        has_element_or_create(j_menu[row[0]][str(row[1])][row[2]], row[3])
        has_element_or_create(j_menu[row[0]][str(row[1])][row[2]][row[3]], row[4])
        has_element_or_create(j_menu[row[0]][str(row[1])][row[2]][row[3]][row[4]], row[5])
        has_element_or_create(j_menu[row[0]][str(row[1])][row[2]][row[3]][row[4]][row[5]], row[6])

        j_menu[row[0]][str(row[1])][row[2]][row[3]][row[4]][row[5]][row[6]] = True

print('making menu values')
make_j_menu_values(j_menu)
print('done menu values')


def get_simple_drop(arr, label):
    ret = []

    for b in arr:
        d = {}
        d['label'] = label + ": " + str(b)
        d['value'] = str(b)
        # print("get_simple_drop, appending: label", label, " value: ", str(b))
        ret.append(d)
    return ret


def get_drop(labels, values, label):
    ret = []
    labels = ["cargo", "shmargo", "id_hyargo"]
    j = len(labels)
    values = [1,2,3]
    for i in range(j):
        d = {}
        d['label'] = label + ": " + str(labels[i])
        d['value'] = str(values[i])
        ret.append(d)

    return ret

