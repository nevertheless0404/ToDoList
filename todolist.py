import datetime as dt
import json
import streamlit as st
import streamlit.components.v1 as components
from streamlit_lottie import st_lottie

# JSON을 읽어 들이는 함수 
def loadJSON(path):
    f = open(path, 'r')
    res = json.load(f)
    f.close()
    return res

# JSON을 저장 
def saveItems(path):
    f = open(path, 'w', encoding='UTF-8')   
    json.dump(items, f, ensure_ascii=False)  
    f.close() 


# ADD/EDIT 버튼의 클릭여부를 반환
def hasClicked(buttonName):
    event = 'clicked' + buttonName.capitalize()
    if event in st.session_state.keys() and st.session_state[event]:
        return True
    else:
        return False

# HTML 만들기 
def makeHTML(x):
    html = '''
    <style>
    div.container {
        border: black double 3px;
        border-radius: 5px;
        width: 100%;
    }

    div.item_pending {
        padding: 2px;
        margin: 2px;
        border-left: green solid 5px; 
        background-color: rgba(0,255,0,0.3);
    }

    div.item_priority {
        padding: 2px;
        margin: 2px;
        border-left: red solid 5px; 
        background-color: rgba(255,0,0,0.3);
    }    

    div.item_done {
        padding: 2px;
        margin: 2px;
        border-left: grey solid 5px; 
        background-color: rgba(128,128,128,0.3);
        text-decoration: line-through;
    }

    .active {
        border: red solid 2px;
        padding: 2px;
        margin: 5px;
    }

    .inactive {
        border: white solid 2px;
        padding: 2px;
        margin: 5px;
    }

    p.desc {
        font-size: 20px;
        margin: 2px 10px;
    }

    p.time {
        font-size: 16px;
        margin: 2px 10px;
    }

    </style>

    <div class="container">

    '''+ x + '</div>'
    return html

# 할일 데이터 가져오기 
items = loadJSON('data.json')

# 현 위치 초기화 
if 'pos' not in st.session_state:
    st.session_state['pos'] = 0


# 로고 Lottie와 타이틀 출력
col1, col2 = st.columns([1,2])
with col1:
    lottie = loadJSON('lottie-load.json')
    st_lottie(lottie, speed=1, loop=True, width=150, height=150)
with col2:
    ''
    ''
    components.html('<div style="font-size:40px; padding:10px;">To Do List</div>', height=100, scrolling=False)

# 메뉴 버튼들과 할일 아이템들을 출력
col1, col2 = st.columns([6,1])

with col1:
    cont1 = st.container()

with col2:
    cont2 = st.container()

with cont1:
    ''
    if st.button('🔺') and not hasClicked('add') and not hasClicked('edit') and st.session_state['pos'] != 0:
        st.session_state['pos'] -= 1

    if st.button('🔻') and not hasClicked('add') and not hasClicked('edit') and st.session_state['pos'] != len(items) -1:
        st.session_state['pos'] += 1

    if st.button('DELETE') and (len(items) !=0):
        pass

# 할 일 아이템들을 한개씩 추가 
temp = ''
for i, item in enumerate(items):
    if i == st.session_state['pos']:
        current = 'active'
    else:
        current = 'inactive'

    status = 'item_' + item['status'].lower()

    temp += f'''<div class="{current}">
                    <div class="{status}">
                        <p class="desc"> {item["description"]} </p>
                        <p class="time"> {item["date"]}  {item["time"]}</p>
                    </div>
                </div>'''
html = makeHTML(temp)

#
# ADD 버튼과 EDIT 버튼 클릭 처리
with cont1:  
    # ADD 버튼 클릭 처리.   
    if hasClicked('add'):
        with st.form(key='myForm1', clear_on_submit=False):
            what = st.text_input('TO DO',placeholder='What do you want to do?')
            when_date = str(st.date_input('DATE',min_value=dt.datetime.today()))
            when_time = str(st.time_input('TIME'))
            status = st.selectbox('STATUS', options=['Pending', 'Priority'])    # 'Done'은 없다!
            if st.form_submit_button('CONFIRM'):
                items.append({'description':what, 'date':when_date, 'time':when_time, 'status': status})
                saveItems('data.json')
                st.session_state['pos'] = len(items) - 1        # 항상 최신 아이템 위치로!
                st.session_state['clickedAdd'] = False
                st.rerun()
            if st.form_submit_button('CANCEL'):
                st.session_state['clickedAdd'] = False
                st.rerun()
    else:
        if cont2.button('ADD'):
            # 'ADD'와 'EDIT'이 동시에 Click된 상태일 수는 없다.
            # if not ('clickedEdit' in st.session_state.keys() and st.session_state['clickedEdit']):
                st.session_state['clickedAdd'] = True     
                st.rerun()

    components.html(html, height=2000, scrolling=False)