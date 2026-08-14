const app = getApp()

Page({
  data: {
    messages: [],
    inputValue: '',
    templates: [],
    activeTemplateCat: 0,
    showTemplates: true,
    showTonguePanel: false,
    tongueImage: '',
    scrollToView: '',
    isSending: false
  },

  onLoad() {
    this.setData({ templates: app.globalData.consultTemplates })

    // 加载历史记录
    const history = wx.getStorageSync('consultHistory')
    if (history && history.length > 0) {
      this.setData({ messages: history, showTemplates: false })
    }

    // 如果有快速问诊问题，自动发送
    const q = app.globalData.quickQuestion
    if (q) {
      app.globalData.quickQuestion = ''
      setTimeout(() => {
        this.sendMessage(q)
      }, 500)
    }

    // 如果有舌诊标记
    if (app.globalData.openTongue) {
      app.globalData.openTongue = false
      setTimeout(() => {
        this.setData({ showTonguePanel: true })
      }, 300)
    }
  },

  onUnload() {
    // 保存问诊记录
    if (this.data.messages.length > 0) {
      wx.setStorageSync('consultHistory', this.data.messages)
      app.globalData.consultHistory = this.data.messages
    }
  },

  // 输入框变化
  onInput(e) {
    this.setData({ inputValue: e.detail.value })
  },

  // 发送消息
  sendMessage(content) {
    const text = content || this.data.inputValue.trim()
    if (!text || this.data.isSending) return

    const userMsg = {
      id: Date.now(),
      role: 'user',
      content: text,
      time: this.formatTime(new Date())
    }

    const messages = [...this.data.messages, userMsg]
    this.setData({
      messages,
      inputValue: '',
      showTemplates: false,
      scrollToView: 'msg-' + userMsg.id,
      isSending: true
    })

    // 模拟AI回复（实际接入后端API）
    this.simulateAIReply(text)
  },

  // 模拟AI回复 - 实际项目中替换为真实API调用
  simulateAIReply(userText) {
    const delay = 800 + Math.random() * 1200

    setTimeout(() => {
      const reply = this.generateMockReply(userText)
      const aiMsg = {
        id: Date.now(),
        role: 'ai',
        content: reply,
        time: this.formatTime(new Date())
      }

      const messages = [...this.data.messages, aiMsg]
      this.setData({
        messages,
        scrollToView: 'msg-' + aiMsg.id,
        isSending: false
      })

      wx.setStorageSync('consultHistory', messages)
      app.globalData.consultHistory = messages
    }, delay)
  },

  // 生成模拟回复
  generateMockReply(text) {
    if (text.includes('舌象') || text.includes('舌诊') || text.includes('舌头')) {
      return '👅 舌诊分析需要您上传舌象照片哦~请点击左下角的相机按钮拍照或从相册选择。\n\n拍摄要点：\n📸 自然光下，面向光源\n👅 舌头自然伸出，不要太用力\n🚫 不要开美颜滤镜\n⏰ 早晨刷牙前拍摄最佳\n\n请先上传舌象照片，我会为您详细分析！'
    }
    if (text.includes('失眠') || text.includes('睡')) {
      return '📋 **辨证分析**\n根据您的描述，初步考虑可能与心脾两虚或肝郁化火有关。失眠在中医看来，常与"心神不宁"相关，就像一锅水烧开了关不了火。\n\n🔍 **进一步了解**\n为了更好地辨证，请问：\n1. 是入睡困难，还是容易醒？\n2. 平时情绪如何？是否容易烦躁？\n3. 舌苔是偏白还是偏黄？\n\n💡 方便的话可以拍张舌象照片，辨证会更精准~'
    }
    if (text.includes('胃') || text.includes('消化') || text.includes('胀')) {
      return '📋 **辨证分析**\n您的症状与"脾胃虚弱"或"肝胃不和"相关。中医讲"脾胃为后天之本"，就像身体的厨房，厨房火力不够，饭就做不熟。\n\n🔍 **进一步了解**\n请问：\n1. 饭后腹胀还是空腹也胀？\n2. 大便情况如何？成形还是偏稀？\n3. 平时喜欢喝热水还是冷水？\n\n💡 方便的话可以拍张舌象，看看舌苔厚薄~'
    }
    if (text.includes('痛经') || text.includes('月经')) {
      return '📋 **辨证分析**\n痛经在中医常见"寒凝血瘀"或"气滞血瘀"两种类型。"通则不痛，痛则不通"，气血运行不畅就会疼痛。\n\n🔍 **进一步了解**\n请问：\n1. 喜暖还是喜凉？热敷会缓解吗？\n2. 血色是鲜红还是暗红？有无血块？\n3. 平时手脚是偏凉还是偏热？\n\n💡 方便的话可以拍张舌象照片，帮助我更准确判断~'
    }
    if (text.includes('疲劳') || text.includes('累') || text.includes('没力气')) {
      return '📋 **辨证分析**\n持续疲劳在中医多与"气虚"相关。气就像身体的电量，气虚就是电量不足，做什么都提不起劲。\n\n🔍 **进一步了解**\n请问：\n1. 是身体乏力还是精神疲惫？\n2. 容易出汗吗？特别是稍微活动就出汗？\n3. 胃口和睡眠怎么样？\n\n请告诉我更多细节，或者拍张舌象照片~'
    }
    if (text.includes('体质') || text.includes('测试')) {
      return '📋 **体质辨识**\n中医将体质分为九种：平和质、气虚质、阳虚质、阴虚质、痰湿质、湿热质、气郁质、血瘀质、特禀质。\n\n🔍 **帮我判断**\n请告诉我以下信息：\n1. 您的出生年份和月份\n2. 平时怕冷还是怕热？\n3. 大便通常是偏干还是偏稀？\n4. 舌苔是偏白还是偏黄？厚还是薄？\n\n我会结合五运六气为您做全面的体质分析！'
    }
    return '📋 感谢您的描述！我是妙手堂AI健康顾问。\n\n🔍 为了更好地为您辨证，请问：\n1. 这个情况持续多久了？\n2. 睡眠和胃口怎么样？\n3. 方便拍张舌象照片吗？（拍摄要点：自然光、不美颜、舌头自然伸出）\n\n请告诉我更多细节，我会为您提供个性化的调理方案。\n\n⚠️ 本内容仅供健康教育参考，不替代医生诊断。'
  },

  // 模板按钮点击
  tapTemplate(e) {
    const prompt = e.currentTarget.dataset.prompt
    this.sendMessage(prompt)
  },

  // 切换模板分类
  switchTemplateCat(e) {
    const idx = e.currentTarget.dataset.idx
    this.setData({ activeTemplateCat: idx })
  },

  // 显示/隐藏舌诊面板
  toggleTonguePanel() {
    this.setData({ showTonguePanel: !this.data.showTonguePanel })
  },

  // 拍照舌象
  takeTonguePhoto() {
    const that = this
    wx.chooseImage({
      count: 1,
      sizeType: ['compressed'],
      sourceType: ['camera'],
      success(res) {
        const tempFilePath = res.tempFilePaths[0]
        that.setData({ tongueImage: tempFilePath, showTonguePanel: false })
        that.sendTongueImage(tempFilePath)
      },
      fail(err) {
        console.log('拍照失败', err)
        wx.showToast({ title: '拍照失败，请重试', icon: 'none' })
      }
    })
  },

  // 从相册选择舌象
  chooseTonguePhoto() {
    const that = this
    wx.chooseImage({
      count: 1,
      sizeType: ['compressed'],
      sourceType: ['album'],
      success(res) {
        const tempFilePath = res.tempFilePaths[0]
        that.setData({ tongueImage: tempFilePath, showTonguePanel: false })
        that.sendTongueImage(tempFilePath)
      },
      fail(err) {
        console.log('选择图片失败', err)
        wx.showToast({ title: '选择失败，请重试', icon: 'none' })
      }
    })
  },

  // 发送舌象图片
  sendTongueImage(tempFilePath) {
    const userMsg = {
      id: Date.now(),
      role: 'user',
      content: '📸 [上传了舌象照片]',
      image: tempFilePath,
      time: this.formatTime(new Date())
    }

    const messages = [...this.data.messages, userMsg]
    this.setData({
      messages,
      showTemplates: false,
      scrollToView: 'msg-' + userMsg.id,
      isSending: true
    })

    // 模拟舌诊分析
    setTimeout(() => {
      const aiMsg = {
        id: Date.now(),
        role: 'ai',
        content: '👅 **舌象初步分析**\n\n📊 四维分析：\n• 舌色：偏淡红\n• 舌形：有轻微齿痕\n• 苔色：薄白\n• 苔质：薄润\n\n🎯 初步判断：舌象显示有轻度脾虚湿盛的倾向，舌边齿痕是脾虚的典型表现。\n\n🔍 请继续描述您的具体症状，我会结合舌象做更全面的辨证分析。\n\n⚠️ 以上为AI初步分析，仅供参考。建议咨询执业中医师确认。',
        time: this.formatTime(new Date())
      }

      const messages = [...this.data.messages, aiMsg]
      this.setData({
        messages,
        scrollToView: 'msg-' + aiMsg.id,
        isSending: false
      })

      wx.setStorageSync('consultHistory', messages)
    }, 1500)
  },

  // 新对话
  newChat() {
    wx.showModal({
      title: '新对话',
      content: '确定要开始新对话吗？当前对话将被清空。',
      success: (res) => {
        if (res.confirm) {
          this.setData({
            messages: [],
            showTemplates: true,
            tongueImage: '',
            inputValue: ''
          })
          wx.removeStorageSync('consultHistory')
          app.globalData.consultHistory = []
          wx.showToast({ title: '已清空对话', icon: 'success' })
        }
      }
    })
  },

  // 格式化时间
  formatTime(date) {
    const h = date.getHours().toString().padStart(2, '0')
    const m = date.getMinutes().toString().padStart(2, '0')
    return h + ':' + m
  },

  // 滚动到底部
  scrollToBottom() {
    if (this.data.messages.length > 0) {
      const last = this.data.messages[this.data.messages.length - 1]
      this.setData({ scrollToView: 'msg-' + last.id })
    }
  },

  // 分享
  onShareAppMessage() {
    return {
      title: '妙手堂AI问诊 - 智能中医健康顾问',
      path: '/pages/consult/consult',
      imageUrl: ''
    }
  }
})
