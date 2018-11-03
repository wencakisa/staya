'use strict'
require('dotenv').config()

const BootBot = require('bootbot')

const bot = new BootBot({
  accessToken: process.env.FB_ACCESS_TOKEN,
  verifyToken: process.env.FB_VERIFY_TOKEN,
  appSecret: process.env.FB_APP_SECRET
})

bot.hear(['hello', 'hi', /hey( there)?/i], (payload, chat) => {
  chat.say('Hello from Staya Chat Bot!')
})

bot.on('attachment', (payload, chat) => {
  let attachment = payload.message.attachments[0]

  if (attachment.type === 'location') {
    let locationTitle = attachment.title
    let locationCoordinates = attachment.payload.coordinates

    console.log('Title: ' + locationTitle)
    console.log('Longitude: ' + locationCoordinates.long)
    console.log('Latitude: ' + locationCoordinates.lat)
  }
})

bot.start()
