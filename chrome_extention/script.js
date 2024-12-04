let DOMAIN = "http://localhost:8080"
let PROJECTLIST = DOMAIN +"/project/list"
let PAGECREATE = DOMAIN +"/page/create/by-project/"

// Background에서 메시지 수신
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  fetchProjects(message.html, message.url);
});

// 프로젝트 목록 가져오는 함수
const fetchProjects = async (content, url) => {
try {
    fetch(PROJECTLIST)
      .then((response) => response.json())
      .then((data) => {        
        projects = data;

        const selectElement = document.createElement("select");
        selectElement.name = "projectSelect";
        selectElement.id = "projectSelect";
    
        // projects 배열을 순회하며 옵션 추가
        projects.forEach(project => {
          const option = document.createElement("option");
          option.value = project.id; // id를 value로 설정
          option.textContent = project.title; // title을 텍스트로 설정
          selectElement.appendChild(option);
        });
        
        // 생성된 select 요소를 HTML에 추가
        document.body.appendChild(selectElement);
        

        const parser = new DOMParser();
        const htmlcontent = parser.parseFromString(content, 'text/html');
        console.log(htmlcontent);

        // 클릭 이벤트 추가
        const button_url = document.getElementById("url");
        button_url.addEventListener("click", ()=>{uploadURL(htmlcontent, url);});
        
        const button_urlhtml = document.getElementById("url_html");
        button_urlhtml.addEventListener("click", ()=>{uploadURLHTML(htmlcontent, url)});
      })
} catch (error) {
    alert("Error fetching project list:", error);
}
};

const uploadURL = async (currentContent, currentUrl) => {
    selector = document.querySelector("#projectSelect");
    project_id = selector.value;
    try {
        const titleText = currentContent.querySelector('title')
            ? currentContent.querySelector('title').innerText 
            : "";
        fetch(PAGECREATE+project_id, {
            method: "POST", // HTTP 메서드 설정
            headers: {
              "Content-Type": "application/json", // JSON 전송임을 명시
            },
            body: JSON.stringify(
                {"title" : titleText, "url" : currentUrl}
            ) // 데이터를 JSON 문자열로 변환하여 전송
        }).then(
            (response) => {
              console.log(response);
              alert("성공적으로 생성되었습니다.");
            }
        );
        
    } catch (error) {
      alert("Error fetching project list:", error);
      console.log("Error fetching project list:", error);
    }
};

const uploadURLHTML = async (currentContent, currentUrl) => {
    selector = document.querySelector("#projectSelect");
    project_id = selector.value;
    try {
        const titleText = currentContent.querySelector('title') 
            ? currentContent.querySelector('title').innerText 
            : "";
        const htmltext = currentContent.querySelector('html').outerHTML;
        fetch(PAGECREATE+project_id, {
            method: "POST", // HTTP 메서드 설정
            headers: {
              "Content-Type": "application/json", // JSON 전송임을 명시
            },
            body: JSON.stringify(
                {"title" : titleText, "url" : currentUrl, "htmlbody" : htmltext, "pagetype":"TEXT"}
            ) // 데이터를 JSON 문자열로 변환하여 전송
        }).then(
            () => {alert("성공적으로 생성되었습니다.");}
        );
    } catch (error) {
      alert("Error fetching project list:", error);
      console.log("Error fetching project list:", error);
    }
};