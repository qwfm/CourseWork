// src/meeting_bot.js
import { ZoomMtg } from "@zoomus/websdk";
import { generate_signature } from "./zoom_signature";
import dotenv from "dotenv";
dotenv.config();

ZoomMtg.setZoomJSLib("https://source.zoom.us/2.14.0/lib", "/av");  
ZoomMtg.preLoadWasm();  
ZoomMtg.prepareWebSDK();

export default class MeetingBot {
  constructor(meetingId, userName = "Bot") {
    this.meetingId = meetingId;
    this.sig = generate_signature(meetingId, 0);
    this.sdkKey = process.env.ZOOM_SDK_KEY;
    this.userName = userName;
  }

  async join() {
    return new Promise((resolve, reject) => {
      ZoomMtg.init({
        leaveUrl: "https://yourdomain.com/leave",
        isSupportChat: true,
        success: () => {
          ZoomMtg.join({
            meetingNumber: this.meetingId,
            userName: this.userName,
            signature: this.sig,
            sdkKey: this.sdkKey,
            passWord: "",
            success: resolve,
            error: reject
          });
        },
        error: reject
      });
    });
  }

  sendMessage(text) {
    ZoomMtg.sendChat({ message: text });
  }

  listenToChat(callback) {
    ZoomMtg.inMeetingServiceListener("onChatMessage", (data) => {
      callback(data);  
    });
  }
}
