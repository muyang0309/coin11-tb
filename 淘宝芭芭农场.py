import time

import uiautomator2 as u2
from uiautomator2 import Direction
from utils import check_chars_exist

in_search = False
unclick_btn = []
is_end = False
error_count = 0
in_other_app = False


def operate_task():
    global in_search
    start_time = time.time()
    taolive_btn = d(resourceId="com.taobao.taobao:id/taolive_close_btn")
    if taolive_btn.exists:
        time.sleep(20)
        while True:
            taolive_btn = d(resourceId="com.taobao.taobao:id/taolive_close_btn")
            if not taolive_btn.exists:
                break
            d.press("back")
            time.sleep(5)
    else:
        while True:
            if time.time() - start_time > 20:
                break
            d.swipe_ext(Direction.FORWARD)
            time.sleep(3)
            d.swipe_ext(Direction.BACKWARD)
            time.sleep(3)
        d.press("back")
        if in_search:
            time.sleep(2)
            in_search = False
            d.press("back")
        if in_other_app:
            # while True:
            time.sleep(0.5)
            d.press("back")


d = u2.connect()
d.app_start("com.taobao.taobao", stop=True)
time.sleep(2)

d.watcher.when("O1CN012qVB9n1tvZ8ATEQGu_!!6000000005964-2-tps-144-144").click()
d.watcher.when(xpath="//android.app.Dialog//android.widget.Button[@text='关闭']").click()
d.watcher.when(xpath="//android.widget.TextView[@package='com.eg.android.AlipayGphone']").click()
d.watcher.start()
farm_btn = d(className="android.widget.FrameLayout", description="芭芭农场", instance=0)
if not farm_btn.click_exists(timeout=10):
    raise Exception("没有找到芭芭农场按钮")
time.sleep(3)
while True:
    fertilize_btn = d(className="android.widget.Button", textContains="集肥料")
    if fertilize_btn.click_exists(timeout=2):
        break
time.sleep(5)
sign_btn = d(className="android.widget.Button", text="去签到")
if sign_btn.exists:
    sign_btn.click()
    time.sleep(2)
while True:
    to_btn = d(className="android.widget.Button", text="去完成")
    if to_btn.exists:
        need_click_view = None
        need_click_index = 0
        task_name = None
        for index, view in enumerate(to_btn):
            text_div = view.sibling(className="android.view.View", instance=0).child(className="android.widget.TextView", instance=0)
            if text_div.exists:
                if check_chars_exist(text_div.get_text()):
                    if view not in unclick_btn:
                        unclick_btn.append(view)
                    continue
                task_name = text_div.get_text()
                need_click_index = index
                need_click_view = view
                break
        if need_click_view:
            print("点击按钮", task_name)
            need_click_view.click()
            time.sleep(2)
            search_view = d(className="android.view.View", text="搜索有福利")
            if search_view.exists:
                d(className="android.widget.EditText", instance=0).send_keys("笔记本电脑")
                d(className="android.widget.Button", text="搜索").click()
                in_search = True
                time.sleep(2)
            web_view = d(className="android.webkit.WebView")
            if web_view.exists(timeout=5):
                operate_task()
        else:
            if not is_end:
                d.swipe_ext(Direction.FORWARD)
                d(scrollable=True).scroll.toEnd()
                is_end = True
            else:
                error_count += 1
                print("未找到可点击按钮", error_count)
                if error_count > 6:
                    break
d.watcher.remove()


