let DOMAIN = "http://localhost:8080"
let PROJECTLIST = DOMAIN +"/project/list"
let PAGECREATE = DOMAIN +"/page/create/by-project/"

chrome.action.onClicked.addListener((tab) => {
  fetch(DOMAIN)
    .then((response) => response.json())
    .then((data) => {
      if (data.isAuthenticated == "true") {
        chrome.windows.create({
          url: "popup.html",
          type: "popup",
          width: 500,
          height: 500,
        });
        // 현재 활성화된 탭에 content script 실행
        chrome.scripting.executeScript(
          {
            target: { tabId: tab.id },
            files: ["content.js"]
          },
          () => {
            // content.js에서 데이터 가져오기
            chrome.tabs.sendMessage(tab.id, { action: "getPageDetails" }, (response) => {
              if (response) {
                // console.log("URL:", response.url);
                // console.log("HTML:", response.html);
                // popup.js로 전달 가능
                chrome.runtime.sendMessage({ url: response.url, html: response.html });
              }
            });
          }
        );
      } else {
        chrome.windows.create({
          url: "error.html",
          type: "popup",
          width: 400,
          height: 500,
        });
      }
    })
    .catch((error) => {
      console.error("Error fetching authentication status:", error);
    });
});


