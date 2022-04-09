# -*- coding: UTF-8 -*-
from pywinauto.application import Application
from pywinauto import mouse
import pprint
import psutil
from pywinauto import clipboard


def processinfo(processName):
    #返回全部进程的list
    pids = psutil.pids()
    for pid in pids:
        #执行psutil.Process(pid)时，这个pid的进程可能已经结束了，因此必须用try
        try:
            p = psutil.Process(pid)
            if p.name() == processName:
                return pid
        except:
            pass





#自绘窗口设置(backend="uia"),使用uia的搜索速度要比win32慢很多，所以能不用就不用

# 对于Windows中自带应用程序，直接执行，对于外部应用应输入完整路径
# 必须用32位的python操纵32位的应用，用64位的python操纵64位的应用，否则可能会出一些奇怪的问题（也可能可以正常运行）
app_uia = Application(backend="uia").start(r'DataGridView_TestApp.exe')
pid=processinfo("DataGridView_TestApp.exe")

#Win32 API窗口设置(backend="win32")，连接要操作程序的PID
app_win32 = Application(backend="win32").connect(process=pid)
#也可以使用标题、类型等匹配,title_re和 class_name这两个可以单独使用也可以一块使用，因为有时没有标题文本，也有时一个窗口类名有多个对象
app_win32 = Application(backend="win32").connect(title_re="Form1")
#连接窗口句柄也可以
#app = Application().connect(handle=0x010f0c)



#title等于pyInspect中的name
#如果找到了多个相同的窗口，可以指定found_index=0,1,2,3
#title是py_inspect中的name属性，部分电脑系统会获取不到title。#title_re=None, # 正则匹配文字
#auto_id是py_inspect中的automation_id属性
#control_type是py_inspect中的control_type属性
#class_name是py_inspect中的class_name属性。#class_name_re=None, # 正则匹配类名
dlg_spec_uia = app_uia.window(title='Form1')
dlg_spec_win32 = app_win32.window(title='Form1')
#获取当前绑定进程的pid
print(dlg_spec_uia.process_id())

#等待控件出现，可传入五种参数, 可以组合传参，但要以空格隔开：
#exists: 窗口变成有效的句柄
#visible: 窗口可见，没有隐藏
#enabled: 窗口没有disable
#ready: visible + enable
#active: active
#timeout:设置超时时间，若在n秒内没有等到窗口在wait_for中传入的几种状态，则会抛出TimeoutError。
#retry_interval:超时后，间隔n秒再次重试。
dlg_spec_win32.wait("exists",timeout=2)

#将窗口最大化
dlg_spec_win32.maximize()


#显示控件树，可用的最佳匹配名显示为树中每个控件的列表，两种模式的控件树是不同的
dlg_spec_uia.print_control_identifiers(filename="tree_uia.txt")
dlg_spec_win32.print_control_identifiers(filename="tree_win32.txt")

#该函数会搜索所有子窗口及孙子窗口，如果找到了多个相同的窗口，可以指定found_index=0,1,2,3
#title是py_inspect中的name属性，部分电脑系统会获取不到title。#title_re=None, # 正则匹配文字
#auto_id是py_inspect中的automation_id属性
#control_type是py_inspect中的control_type属性
#class_name是py_inspect中的class_name属性。#class_name_re=None, # 正则匹配类名
cj_uia=dlg_spec_uia.child_window(auto_id="textBox1", control_type="Edit")
cj_uia.wait("exists",timeout=2)
cj_uia.print_control_identifiers()


cj_win32=dlg_spec_win32.child_window(auto_id="textBox1",class_name="WindowsForms10.EDIT.app.0.141b42a_r7_ad1")
cj_win32.wait("exists",timeout=2)
cj_win32.print_control_identifiers()


#显示此控件的属性及支持的操作
pprint.pprint(dir(cj_uia.wrapper_object()))
pprint.pprint(dir(cj_uia.element_info))
print("title:",cj_uia.element_info.name)
print("auto_id:",cj_uia.element_info.automation_id)
print("control_type:",cj_uia.element_info.control_type)
print("class_name:",cj_uia.element_info.class_name)



#可以省略wrapper_object()
# 给控件画个红色框便于看出是哪个,支持'red', 'green', 'blue'
cj_uia.wrapper_object().draw_outline(colour = 'red')
cj_win32.wrapper_object().draw_outline(colour = 'green')

cj_uia.wrapper_object().set_edit_text("我是uia")
#print(cj_uia.exists())
cj_win32.wrapper_object().set_edit_text("我是win32")

#可以省略wrapper_object()
#uia模式下方法
print(cj_uia.wrapper_object().legacy_properties().get('Value'))
#win32模式下的方法
print(cj_win32.wrapper_object().text_block())


#显示菜单,这个程序只能用uia后端操纵菜单
menu=dlg_spec_uia["menu"].items()
pprint.pprint(menu)
#多级菜单的操作方法,可以用索引，也可以用title，这个例子因为有多个title相同，所以用了索引。这个程序只能用uia后端操纵菜单
dlg_spec_uia.menu_select("tem1->#1->#1")


cj3=dlg_spec_uia.child_window(title="AddCol", auto_id="button2", control_type="Button").wrapper_object()
#模拟鼠标点击
cj3.click_input()
#通过消息进行后台点击,有的程序点击无反应时切换后端进行尝试
cj3.click()

#win32后端的control_type属性与uia模式下不同
cj3=dlg_spec_win32.child_window(title="AddCol", auto_id="button2", control_type="System.Windows.Forms.Button").wrapper_object()
#模拟鼠标双击
cj3.double_click_input()
#通过消息进行后台点击,有的程序点击无反应时切换后端进行尝试
cj3.click()


#win32模式
ComboBox=dlg_spec_win32.child_window(auto_id="comboRowType", control_type="System.Windows.Forms.ComboBox").wrapper_object()
#通过消息进行后台点击,有的程序点击无反应时切换后端进行尝试
ComboBox.select(1)
ComboBox.select("Numbers")
print(ComboBox.item_texts())
print(ComboBox.selected_text())

#uia模式下必须先将combbox先展开才能选择，可以用以下几种方式（不一定都适用）
ComboBox=dlg_spec_uia.child_window(auto_id="comboRowType", control_type="ComboBox").wrapper_object()
ComboBox.type_keys("%{DOWN}")
#ComboBox.expand()
#ComboBox.click_input()

#然后再选择，可以用以下几种方式（不一定都适用）
#ComboBox.child_window(title="Letters", control_type="ListItem").click_input()
ComboBox.select(1)
#ComboBox.wrapper_object().select("Numbers")
print(ComboBox.texts())
print(ComboBox.selected_text())


mouse.click(button='left', coords=(100,100))
a=input("")








