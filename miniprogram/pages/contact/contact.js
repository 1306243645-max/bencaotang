const app = getApp()
Page({
  data: {
    phone: app.globalData.phone,
    wechat: app.globalData.wechat,
    email: app.globalData.email,
    address: app.globalData.address,
  },
  callPhone(){ wx.makePhoneCall({phoneNumber: this.data.phone}) },
  copyWechat(){
    wx.setClipboardData({data: this.data.wechat})
    wx.showToast({title:'微信号已复制',icon:'success'})
  },
  goConsult(){ wx.switchTab({url:'/pages/consult/consult'}) },
})
