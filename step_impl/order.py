#coding=utf8
from getgauge.python import step
from step_impl.pages.order_Page import Order_Page

class orderStart:
    OrderPage = Order_Page()


@step("login Interface TestCase")
def login_interface_testcase():
    status = orderStart.OrderPage.login()
    assert status
