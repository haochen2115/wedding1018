const express = require('express')
const fs = require('fs')
const path = require('path')

const app = express()

app.use('/public', express.static(path.join(__dirname, 'public')))

app.get('/', function (req, res) {
  try {
    let html = fs.readFileSync(path.join(__dirname, 'index.html'), 'utf-8')
    res.header('Content-Type', 'text/html;charset=utf-8');
    res.send(html)
  } catch (error) {
    console.error('Error reading index.html:', error)
    res.status(500).send('Internal Server Error')
  }
})

const port = process.env.PORT || 8081

// 本地开发时启动服务器
if (require.main === module) {
  app.listen(port, () => { 
    console.log(`服务器启动成功！端口: ${port}`)
  })
}

// 导出给Vercel使用
module.exports = app