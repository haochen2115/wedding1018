const express = require('express')
const fs = require('fs')

const app = express()

app.use('/public',express.static('public'))

app.get('/', function (req, res) {
  let html = fs.readFileSync('./index.html','utf-8')
  res.header('Content-Type', 'text/html;charset=utf-8');
  res.send(html)
})

app.listen(8081, '0.0.0.0', () => { 
  console.log('服务器启动成功！')
  console.log('本地访问: http://localhost:8081')
  console.log('局域网访问: http://你的电脑IP:8081')
  console.log('请确保手机和电脑在同一个WiFi网络下')
})