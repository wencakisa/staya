'use strict'

require('dotenv').config()
const axios = require('axios')
const BootBot = require('bootbot')

const bot = new BootBot({
  accessToken: process.env.FB_ACCESS_TOKEN,
  verifyToken: process.env.FB_VERIFY_TOKEN,
  appSecret: process.env.FB_APP_SECRET
})

const botPort = 3030
const baseAPIUrl = 'http://localhost:8000/api/v1/'
const baseClientUrl = 'http://localhost:3000/'

bot.setGreetingText('Hello, I am Staya Chat Bot! With me you can easily operate with Staya app directly from your Messenger! :)')

bot.hear(['hello', 'hi', /hey( there)?/i], (payload, chat) => {
  chat.say('Hello from Staya Chat Bot!')
})

bot.on('attachment', (payload, chat) => {
  let attachment = payload.message.attachments[0]

  if (attachment.type === 'location') {
    let locationTitle = attachment.title

    let locationCoordinates = attachment.payload.coordinates
    let long = locationCoordinates.long
    let lat = locationCoordinates.lat

    let url = `${baseAPIUrl}listings?near_long=${long}&near_lat=${lat}`

    axios.get(url)
      .then((resp) => {
        chat.say(`Showing you listings nearby ${locationTitle}...`)

        let chatElements = []
        resp.data.forEach(listing => {
          let listingUrl = `${baseClientUrl}listings/${listing.id}`

          chatElements.push({
            title: listing.title,
            subtitle: listing.description,
            image_url: listing.images[0].image,
            default_action: {
              type: 'web_url',
              url: listingUrl
            },
            buttons: [
              {
                title: 'Book now',
                type: 'web_url',
                url: listingUrl
              }
            ]
          })
        })

        chat.say({
          top_element_style: 'COMPACT',
          elements: chatElements,
          buttons: []
        })
      })
      .catch((err) => {
        console.log(err)
      })
  }
})

bot.start(botPort)
