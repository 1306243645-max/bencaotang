const app = getApp()

Page({
  data: {
    userInfo: {
      avatar: '',
      nickName: '',
      phone: ''
    },
    stats: {
      consults: 0,
      orders: 0,
      bookings: 0
    },
    contactInfo: {
      phone: app.globalData.phone,
      wechat: app.globalData.wechat,
      clinicName: app.globalData.clinicName
    }
  },

  onShow() {
    this.loadUserInfo()
    this.loadStats()
  },

  onLoad() {
    this.loadUserInfo()
    this.loadStats()
  },

  // 加载用户信息
  loadUserInfo() {
    const userInfo = wx.getStorageSync('userInfo')
    if (userInfo) {
      this.setData({ userInfo })
    }
  },

  // 加载统计数据
  loadStats() {
    const consultHistory = wx.getStorageSync('consultHistory') || []
    const orders = wx.getStorageSync('myOrders') || []
    const bookings = wx.getStorageSync('myBookings') || []

    this.setData({
      stats: {
        consults: consultHistory.length > 0 ? Math.ceil(consultHistory.length / 2) : 0,
        orders: orders.length,
        bookings: bookings.length
      }
    })
  },

  // 登录/获取用户信息
  handleLogin() {
    wx.getUserProfile({
      desc: '用于完善个人资料',
      success: (res) => {
        const userInfo = {
          avatar: res.userInfo.avatarUrl,
          nickName: res.userInfo.nickName,
          phone: ''
        }
        this.setData({ userInfo })
        wx.setStorageSync('userInfo', userInfo)

        // 获取手机号
        wx.showModal({
          title: '完善信息',
          content: '是否绑定手机号，方便我们联系您？',
          success: (modalRes) => {
            if (modalRes.confirm) {
              // 微信手机号授权需通过 button open-type="getPhoneNumber"
              wx.showToast({ title: '请在弹窗中授权手机号', icon: 'none' })
            }
          }
        })
      },
      fail: () => {
        wx.showToast({ title: '已取消登录', icon: 'none' })
      }
    })
  },

  // 获取手机号（通过 button open-type）
  getPhoneNumber(e) {
    if (e.detail.encryptedData) {
      // 实际项目需发送到后端解密
      const userInfo = { ...this.data.userInfo, phone: '已绑定' }
      this.setData({ userInfo })
      wx.setStorageSync('userInfo', userInfo)
      wx.showToast({ title: '手机号已绑定', icon: 'success' })
    }
  },

  // 导航
  goConsultHistory() {
    wx.showToast({ title: '问诊记录开发中', icon: 'none' })
  },

  goConstitution() {
    wx.showToast({ title: '体质报告开发中', icon: 'none' })
  },

  goOrders() {
    wx.showToast({ title: '订单功能开发中', icon: 'none' })
  },

  goBookings() {
    wx.showToast({ title: '预约记录开发中', icon: 'none' })
  },

  goFavorites() {
    wx.showToast({ title: '收藏功能开发中', icon: 'none' })
  },

  goAbout() {
    wx.showModal({
      title: '关于本草堂',
      content: '山东本草堂中医诊所\n\n三代中医世家传承\nAI智能问诊 · 22个知识库\n五运六气 · 面诊 · 舌诊\n\n版本：v1.0.0\n\n🌿 本草济世 · 仁心济世',
      showCancel: false,
      confirmText: '我知道了'
    })
  },

  // 分享
  onShareAppMessage() {
    return {
      title: '本草堂中医诊所 - AI智能中医问诊',
      path: '/pages/index/index',
      imageUrl: ''
    }
  },

  shareApp() {
    wx.showToast({ title: '点击右上角分享给朋友', icon: 'none' })
  },

  // 拨打电话
  callPhone() {
    wx.makePhoneCall({ phoneNumber: app.globalData.phone })
  },

  // 复制微信
  copyWechat() {
    wx.setClipboardData({
      data: app.globalData.wechat,
      success() {
        wx.showToast({ title: '微信已复制: ' + app.globalData.wechat, icon: 'success' })
      }
    })
  }
})
