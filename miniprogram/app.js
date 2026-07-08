App({
  globalData: {
    webUrl: 'http://172.20.21.34:8501',
    phone: '18254191315',
    wechat: '18254191315',
    email: '83497212@qq.com',
    address: '山东省济南市历下区经十路123号',
    clinicName: '山东本草堂中医诊所',
    slogan: '本草济世 · 仁心济世',
    hours: '周一至周五 8:30-17:30 | 周六 9:00-16:00',
    quickQuestion: '',

    // 名医团队数据
    experts: [
      {
        id: 1,
        icon: '🏔️',
        avatar: '',
        name: '张树淮 先生',
        title: '金锁玉关风水第三代传承人',
        field: '风水堪舆 · 八字命理',
        desc: '金锁玉关风水学正宗传承人，张秩也老师祖父。精通八卦砂水法、二十四山向，数百实战案例验证。',
        tags: ['风水堪舆', '八字命理', '金锁玉关']
      },
      {
        id: 2,
        icon: '📚',
        avatar: '',
        name: '张秩也 老师',
        title: '金锁玉关风水讲师',
        field: '风水教学 · 实战案例',
        desc: '24课完整体系，数百实战案例。将家传金锁玉关风水学系统化教学，深入浅出，易学易懂。',
        tags: ['风水教学', '实战案例', '系统课程']
      },
      {
        id: 3,
        icon: '🌟',
        avatar: '',
        name: '毛小妹 老师',
        title: '五运六气研究专家',
        field: '五运六气 · 人体气象站',
        desc: '创立毛氏运气医学体系，人体气象站理论创始人。将千年运气学说与现代生活结合，精准体质分析。',
        tags: ['五运六气', '人体气象站', '运气医学']
      },
      {
        id: 4,
        icon: '🤖',
        avatar: '',
        name: '本草堂AI团队',
        title: 'AI问诊知识库专家组',
        field: '中医学 · AI融合',
        desc: '22个专业知识库，涵盖中医全科。结合经典中医理论与AI技术，提供24小时在线智能辨证服务。',
        tags: ['AI问诊', '知识库', '智能辨证']
      }
    ],

    // 养生产品数据
    products: [
      { id: 1, icon: '🍵', name: '菊花枸杞茶包', price: 12, tag: '热销', desc: '清肝明目，10包装', category: '茶饮' },
      { id: 2, icon: '🌹', name: '玫瑰红枣养颜茶', price: 15, tag: '女性必备', desc: '疏肝养血，10包装', category: '茶饮' },
      { id: 3, icon: '🍲', name: '四神汤料包', price: 12, tag: '全家适用', desc: '健脾祛湿，4人份', category: '汤料' },
      { id: 4, icon: '🍯', name: '秋梨膏', price: 25, tag: '秋季必囤', desc: '润肺止咳，250g/瓶', category: '膏方' },
      { id: 5, icon: '🥜', name: '黑芝麻核桃粉', price: 20, tag: '男士推荐', desc: '补肾乌发，300g/罐', category: '粉剂' },
      { id: 6, icon: '🍬', name: '阿胶糕', price: 35, tag: '口碑爆款', desc: '补血养颜，250g/盒', category: '膏方' },
      { id: 7, icon: '🦶', name: '安神助眠泡脚包', price: 15, tag: '失眠救星', desc: '宁心安神，5次量', category: '外用' },
      { id: 8, icon: '🔥', name: '艾叶生姜泡脚包', price: 10, tag: '冬季必备', desc: '温经散寒，7次量', category: '外用' },
      { id: 9, icon: '🫚', name: '陈皮生姜暖胃茶', price: 10, tag: '口碑好', desc: '温中散寒，10包装', category: '茶饮' },
      { id: 10, icon: '💎', name: '花旗参石斛汤料', price: 25, tag: '高端滋补', desc: '益气养阴，4人份', category: '汤料' },
      { id: 11, icon: '🍰', name: '八珍糕', price: 18, tag: '老少皆宜', desc: '健脾养胃，12块/盒', category: '糕点' },
      { id: 12, icon: '🫐', name: '桑葚膏', price: 22, tag: '养发', desc: '滋阴补血，250g/瓶', category: '膏方' }
    ],

    // 快速问诊模板
    consultTemplates: [
      { category: '睡眠问题', icon: '😴', items: [
        { label: '入睡困难多梦', prompt: '入睡困难，多梦易醒，心慌健忘，是什么中医证型？怎么调理？' },
        { label: '凌晨1-3点醒', prompt: '每天凌晨1-3点准时醒，醒来口干口苦，烦躁，中医怎么看？' },
        { label: '半夜醒+盗汗', prompt: '睡着后半夜总醒，手心脚心发热，盗汗，口干，是什么阴虚？' }
      ]},
      { category: '消化问题', icon: '🍽️', items: [
        { label: '饭后腹胀乏力', prompt: '饭后腹胀，浑身乏力，大便稀不成形，是什么脾胃问题？' },
        { label: '胃酸烧心', prompt: '胃酸反流烧心，打嗝，吃什么都不消化，中医怎么调理？' },
        { label: '便秘', prompt: '长期便秘，大便干结如羊粪，口干，吃什么能改善？' }
      ]},
      { category: '女性健康', icon: '👩', items: [
        { label: '痛经怕冷', prompt: '月经痛，喜暖怕冷，血色暗有血块，得热痛减，怎么调理？' },
        { label: '经前烦躁', prompt: '月经前乳房胀痛，烦躁易怒，情绪波动大，中医怎么疏肝？' },
        { label: '更年期潮热', prompt: '更年期一阵阵发热出汗，心烦失眠，口干，怎么滋阴？' }
      ]},
      { category: '体质调理', icon: '💪', items: [
        { label: '总是疲劳', prompt: '总是感觉很累，说话都没力气，稍微活动就出汗，怎么补气？' },
        { label: '手脚冰凉', prompt: '一年四季手脚冰凉，特别怕冷，是什么阳虚？怎么调理？' },
        { label: '脸油长痘', prompt: '脸上爱出油长痘，口苦口臭，大便粘滞，是什么湿热？' }
      ]},
      { category: '养生咨询', icon: '🌿', items: [
        { label: '体质测试', prompt: '我想知道自己是哪种中医体质，帮我分析一下。我的出生年份是____' },
        { label: '夏季养生', prompt: '三伏天怎么养生？清热祛湿有什么好方法？推荐什么茶饮？' },
        { label: '日常茶饮', prompt: '根据我的体质，推荐一款日常喝的养生茶。我平时容易____' }
      ]}
    ],

    // 购物车
    cart: [],

    // 问诊记录
    consultHistory: [],

    // 预约记录
    bookings: [],

    // 订单记录
    orders: [],

    // 用户信息
    userInfo: null
  },

  onLaunch() {
    console.log('本草堂小程序启动')
    // 读取本地存储的购物车
    const cart = wx.getStorageSync('cart')
    if (cart) this.globalData.cart = cart
    // 读取问诊记录
    const history = wx.getStorageSync('consultHistory')
    if (history) this.globalData.consultHistory = history
  }
})
