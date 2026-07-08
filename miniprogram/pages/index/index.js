const app = getApp()

Page({
  data: {
    clinicName: '山东本草堂中医诊所',
    slogan: '本草济世 · 仁心济世',
    features: [
      {
        icon: '🌿',
        title: '三代中医传承',
        desc: '山东中医世家，三代人专注中医诊疗，将正宗的中医智慧带给每一位患者。'
      },
      {
        icon: '🤖',
        title: 'AI + 中医',
        desc: '自研AI问诊系统，22个知识库，24小时在线健康咨询，智能体质辨识。'
      },
      {
        icon: '💚',
        title: '专业服务',
        desc: '针灸、中药、推拿、食疗，全方位中医健康服务，总有一种适合你。'
      }
    ],
    contactInfo: {
      phone: app.globalData.phone,
      wechat: app.globalData.wechat,
      address: app.globalData.address
    }
  },

  onLoad() {
    // 检查是否有快速问诊问题要传递
    const q = app.globalData.quickQuestion
    if (q) {
      app.globalData.quickQuestion = ''
    }
  },

  onShareAppMessage() {
    return {
      title: '本草堂中医诊所 - AI智能问诊',
      path: '/pages/index/index',
      imageUrl: ''
    }
  },

  // 导航到各功能页
  goConsult() {
    wx.switchTab({ url: '/pages/consult/consult' })
  },

  goTongue() {
    app.globalData.openTongue = true
    wx.switchTab({ url: '/pages/consult/consult' })
  },

  goExperts() {
    wx.switchTab({ url: '/pages/experts/experts' })
  },

  goShop() {
    wx.switchTab({ url: '/pages/shop/shop' })
  },

  goMine() {
    wx.switchTab({ url: '/pages/mine/mine' })
  },

  // 快速问诊标签点击
  quickAsk(e) {
    const q = e.currentTarget.dataset.q
    app.globalData.quickQuestion = q
    wx.switchTab({ url: '/pages/consult/consult' })
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
        wx.showToast({ title: '微信已复制', icon: 'success' })
      }
    })
  }
})
