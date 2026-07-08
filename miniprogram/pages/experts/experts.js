const app = getApp()

Page({
  data: {
    experts: [],
    institutions: [
      {
        icon: '🏛️',
        name: '山东中医药大学附属',
        subtitle: '山东省中医院',
        desc: '临床教学合作单位，提供专家资源与学术支持'
      },
      {
        icon: '🔬',
        name: '中国中医科学院',
        subtitle: '中医药信息研究所',
        desc: '中医药信息化研究合作，知识库共建'
      },
      {
        icon: '🌏',
        name: '世界中医药学会联合会',
        subtitle: '中医适宜技术委员会',
        desc: '国际中医标准推广与学术交流合作'
      }
    ]
  },

  onLoad() {
    this.setData({ experts: app.globalData.experts })
  },

  // 查看专家详情
  tapExpert(e) {
    const expert = e.currentTarget.dataset.expert
    wx.showModal({
      title: expert.name,
      content: expert.title + '\n\n专长：' + expert.field + '\n\n' + expert.desc,
      confirmText: '联系咨询',
      cancelText: '关闭',
      success(res) {
        if (res.confirm) {
          wx.makePhoneCall({ phoneNumber: app.globalData.phone })
        }
      }
    })
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
  },

  onShareAppMessage() {
    return {
      title: '本草堂名医团队 - 三代传承 · 名医荟萃',
      path: '/pages/experts/experts',
      imageUrl: ''
    }
  }
})
