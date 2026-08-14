const app = getApp()

Page({
  data: {
    products: [],
    cart: [],
    cartCount: 0,
    showCart: false,
    categories: ['全部', '茶饮', '汤料', '膏方', '粉剂', '外用', '糕点'],
    activeCategory: 0
  },

  onLoad() {
    this.loadProducts()
    this.loadCart()
  },

  onShow() {
    this.loadCart()
  },

  // 加载商品
  loadProducts() {
    this.setData({ products: app.globalData.products })
  },

  // 加载购物车
  loadCart() {
    const cart = wx.getStorageSync('cart') || []
    this.setData({
      cart: cart,
      cartCount: cart.reduce((sum, item) => sum + item.qty, 0)
    })
    app.globalData.cart = cart
  },

  // 切换分类
  switchCategory(e) {
    const idx = e.currentTarget.dataset.idx
    this.setData({ activeCategory: idx })
  },

  // 筛选商品
  getFilteredProducts() {
    if (this.data.activeCategory === 0) {
      return this.data.products
    }
    const cat = this.data.categories[this.data.activeCategory]
    return this.data.products.filter(p => p.category === cat)
  },

  // 加入购物车
  addToCart(e) {
    const product = e.currentTarget.dataset.product
    const cart = [...this.data.cart]
    const existIdx = cart.findIndex(item => item.id === product.id)

    if (existIdx >= 0) {
      cart[existIdx].qty += 1
    } else {
      cart.push({
        id: product.id,
        name: product.name,
        icon: product.icon,
        price: product.price,
        qty: 1
      })
    }

    this.setData({ cart, cartCount: cart.reduce((s, i) => s + i.qty, 0) })
    wx.setStorageSync('cart', cart)
    app.globalData.cart = cart

    wx.showToast({
      title: '已加入购物车',
      icon: 'success',
      duration: 1000
    })
  },

  // 切换购物车面板
  toggleCart() {
    this.setData({ showCart: !this.data.showCart })
  },

  // 增加数量
  increaseQty(e) {
    const id = e.currentTarget.dataset.id
    const cart = this.data.cart.map(item => {
      if (item.id === id) item.qty += 1
      return item
    })
    this.setData({ cart, cartCount: cart.reduce((s, i) => s + i.qty, 0) })
    wx.setStorageSync('cart', cart)
    app.globalData.cart = cart
  },

  // 减少数量
  decreaseQty(e) {
    const id = e.currentTarget.dataset.id
    let cart = this.data.cart.map(item => {
      if (item.id === id && item.qty > 1) item.qty -= 1
      return item
    })
    // 移除数量为0的
    cart = cart.filter(item => item.qty > 0)
    this.setData({ cart, cartCount: cart.reduce((s, i) => s + i.qty, 0) })
    wx.setStorageSync('cart', cart)
    app.globalData.cart = cart
  },

  // 清空购物车
  clearCart() {
    wx.showModal({
      title: '清空购物车',
      content: '确定要清空购物车吗？',
      success: (res) => {
        if (res.confirm) {
          this.setData({ cart: [], cartCount: 0 })
          wx.setStorageSync('cart', [])
          app.globalData.cart = []
          wx.showToast({ title: '已清空', icon: 'success' })
        }
      }
    })
  },

  // 提交订单
  submitOrder() {
    if (this.data.cart.length === 0) {
      wx.showToast({ title: '购物车为空', icon: 'none' })
      return
    }

    const total = this.data.cart.reduce((sum, item) => sum + item.price * item.qty, 0)
    const items = this.data.cart.map(item => item.name + ' x' + item.qty).join(', ')

    wx.showModal({
      title: '确认下单',
      content: items + '\n\n合计：¥' + total + '\n\n下单后请通过微信联系客服确认订单和配送信息。',
      confirmText: '确认下单',
      cancelText: '再看看',
      success: (res) => {
        if (res.confirm) {
          // 保存订单
          const orders = wx.getStorageSync('orders') || []
          orders.push({
            items: this.data.cart,
            total: total,
            time: new Date().toLocaleString(),
            status: '待确认'
          })
          wx.setStorageSync('orders', orders)
          app.globalData.orders = orders

          // 清空购物车
          this.setData({ cart: [], cartCount: 0, showCart: false })
          wx.setStorageSync('cart', [])
          app.globalData.cart = []

          wx.showToast({
            title: '下单成功！请微信联系客服确认',
            icon: 'none',
            duration: 2500
          })

          // 延迟复制微信
          setTimeout(() => {
            wx.setClipboardData({
              data: app.globalData.wechat,
              success() {
                wx.showToast({ title: '客服微信已复制', icon: 'none' })
              }
            })
          }, 2000)
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
      title: '妙手堂养生商城 - 药食同源 · 精选好物',
      path: '/pages/shop/shop',
      imageUrl: ''
    }
  }
})
