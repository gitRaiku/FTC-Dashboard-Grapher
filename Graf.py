#!/bin/python3 

import websockets
import asyncio
import json
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib import style
from collections import deque
import time
import math
from random import random
import os
import sys

CLOSE = False
TOUT = 10
# var = ['x', 'y', 'xError', 'yError', 'heading (deg)']
# var = ['CycleTime']
# var = ['CT0', 'CT1', 'CT2', 'CT3', 'CT4', 'CT5', 'CT6', 'CT7', 'CT8']
# var = ['CT5']
# var = ['heading (deg)']
var = ['ver', 'vel', 'vef']
# var = ['EVl', 'EVr', 'EVf']
# var = ['Che']
# var = ['Ef', 'El', 'Er']
# var = ['Ex', 'Ey', 'Eh']
# var = ['xError'] # , 'yError']#, 'headingError (deg)']
# var = ['vref', 'v0']
# var = ['Current', 'Target']
# var = ['Power']
# var = ['measuredVelocity', 'targetVelocity']
x = []
y = []
bat = 0

for i in var:
    x.append(deque())
    y.append(deque())

def gt():
    return time.time()

def redr():
    plt.show()
    plt.pause(0.001)

def shut(event):
    #print(f'A{CLOSE}')
    CLOSE = True
    #print(f'A{CLOSE}')

def dequetl(dq):
    a = []
    for i in dq:
        a.append(i)
    return a

def fff(dql):
    r = []
    for i in dql:
        r.append(dequetl(i))
    return r

async def plot_t():
    # style.use('fivethirtyeight')
    CLOSE = False
    s = gt()

    plt.ion()
    plt.rcParams['toolbar'] = 'none'
    fig = plt.figure()
    # fig.canvas.manager.toolmanager.remove_tool("forwar")
    ax = fig.add_subplot(1, 1, 1)
    fig.canvas.mpl_connect('close_event', shut)
    while not CLOSE:
        #print(f'1{CLOSE}')
        try:
            ax.clear()
            # mc = (random(), random(), random())
            # ax.plot(y, x, color=mc)
            if len(var) == 0:
                ax.plot([], [], label='', alpha=0.0)
                ax.legend(loc = 'upper right')
            else:
                # y = [[1, 2, 3], []]
                # x = [[1, 2, 3], []]
                for i in range(len(var)):
                    ax.plot(y[i], x[i], label=var[i], alpha=0.7)
                    ax.legend(loc = 'upper right')
                    ax.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
            redr()
            await asyncio.sleep(0.01)
        except:
            if len(sys.argv) < 2:
                t = int(time.time()) - (int(time.time()) // 1000) * 1000
                try:
                    print(f'Dumping to {t}.json')
                    with open(f'{t}.json', 'w') as ff:
                        f = json.dumps({'vars': var, 'elemsx': fff(x), 'elemsy': fff(y)})
                        print(f, file=ff)
                except:
                    try:
                        print(f'Remove {t}.json')
                        os.remove(f'{t}.json')
                    except Exception as e:
                        print(e)
                        pass
            CLOSE = True
    #print(f'2{CLOSE}')

async def p1(wb):
    ct = gt()
    CLOSE = False
    while not CLOSE:
        #print(f'2{CLOSE}')
        try:
            if gt() - ct > 3.0:
                await wb.send('{type: "GET_ROBOT_STATUS"}')
                ct = gt()
            await asyncio.sleep(0.4)
        except:
            print('AAAAAAAA')
            CLOSE = True
    #print(f'2{CLOSE}')

async def p2(wb):
    it = gt()
    CLOSE = False
    await wb.send('{type: "GET_ROBOT_STATUS"}')
    while not CLOSE:
        #print(f'3{CLOSE}')
        try: 
            async for resp in wb:
                r = json.loads(resp)
                for i in range(len(var)):
                    while len(y[i]) > 0 and y[i][-1] - y[i][0] > TOUT:
                        x[i].popleft()
                        y[i].popleft()

                # print(r)
                if r['type'] == "RECEIVE_TELEMETRY":
                    for tel in r['telemetry']:
                        for nm in tel['data']:
                            if nm == 'bat':
                                bat = int(tel['data'][var[var.index(nm)]])
                                print(f'Battery {bat}')
                            if nm in var:
                                idx = var.index(nm)
                                x[idx].append(float(tel['data'][var[idx]]))
                                y[idx].append(tel['timestamp'] / 1000)
                                # print(f'Got for {var[idx]}: {x[idx][-1]} at {y[idx][-1]}')
                            else:
                                pass
                                # print(f'Could not find {nm}')
            await asyncio.sleep(0.0001)
        except Exception as e:
            print("AAAAAAAA")
            CLOSE = True

async def p3(wb):
    b = ['Test', 'Autonoooooooooom']
    CLOSE = False
    while not CLOSE:
        #print(f'4{CLOSE}')
        try:
            a = input().split(' ')
            print(a)
            if a[0] == 'run':
                print(f'{{"type": "INIT_OP_MODE", "opModeName": "{b[int(a[1])]}"}}')
                await wb.send(f'{{"type": "INIT_OP_MODE", "opModeName": "{b[int(a[1])]}"}}')
                if input() != 'end':
                    print(f'{{"type": "START_OP_MODE"}}')
                    await wb.send(f'{{"type": "START_OP_MODE"}}')
                else:
                    print(f'{{"type": "STOP_OP_MODE"}}')
                    await wb.send(f'{{"type": "STOP_OP_MODE"}}')
            elif a[0] == 'end':
                print(f'{{"type": "STOP_OP_MODE"}}')
                await wb.send(f'{{"type": "STOP_OP_MODE"}}')
            else:
                print(f'Unknown command {a}!')
            await asyncio.sleep(0.0001)
        except:
            print("AAAAAAAA")
            CLOSE = True

async def webs():
    adr = 'ws://192.168.43.1:8000/'

    async with websockets.connect(adr) as wb:
        t1 = asyncio.create_task(p1(wb))
        t2 = asyncio.create_task(p2(wb))
        # t3 = asyncio.create_task(p3(wb))

        await t1


async def main():
    tas1 = asyncio.create_task(plot_t())
    tas2 = asyncio.create_task(webs())

    await tas1

asyncio.run(main())

