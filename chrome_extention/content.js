// 현재 페이지의 URL과 HTML 가져오기
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "getPageDetails") {
    const pageDetails = {
      url: window.location.href,
      html: document.documentElement.outerHTML
    };
    sendResponse(pageDetails);
  }
});