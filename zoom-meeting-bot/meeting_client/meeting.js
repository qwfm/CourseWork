function parseQuery() {
    const params = {};
    location.search.slice(1).split("&").forEach(pair => {
      const [key, value] = pair.split("=");
      params[key] = decodeURIComponent(value);
    });
    return params;
  }
  
  const { mn, sig, sdkKey, userName } = parseQuery();
  
  ZoomMtg.setZoomJSLib('https://source.zoom.us/2.18.0/lib', '/av');
  ZoomMtg.preLoadWasm(); 
  ZoomMtg.prepareJssdk();
  
  ZoomMtg.init({
    leaveUrl: window.location.href,
    success: () => {
      ZoomMtg.join({
        meetingNumber: mn,
        signature: sig,
        sdkKey: sdkKey,
        userName: userName || "Bot",
        passWord: "",
        success: () => console.log("Bot joined meeting"),
        error: (e) => console.error(e)
      });
    }
  });
  
  function sendBotChat() {
    const msg = document.getElementById("chatInput").value;
    ZoomMtg.sendChat({ message: msg })
      .then(() => console.log("Sent:", msg))
      .catch(console.error);
  }
  