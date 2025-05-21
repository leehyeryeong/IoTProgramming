// Firebase 초기화
const firebaseConfig = {
  apiKey: "AIzaSyDXz0ksdfYD5Rt4P4y8e1YIbbgr8OBhZlw",
  authDomain: "test-6d110.firebaseapp.com",
  databaseURL: "https://test-6d110-default-rtdb.asia-southeast1.firebasedatabase.app",
  projectId: "test-6d110",
  storageBucket: "test-6d110.firebasestorage.app",
  messagingSenderId: "1066690464338",
  appId: "1:1066690464338:web:14f34baa5953317fa82d8b"
};

// Firebase 초기화
firebase.initializeApp(firebaseConfig);
const database = firebase.database();

// LED 제어 함수들
function ledON() {
  console.log("LED ON");
  document.getElementById("img").src = "ledOn.png"; // 즉시 반영
  database.ref('led').set({
    led: 1
  });
}

function ledOFF() {
  console.log("LED OFF");
  document.getElementById("img").src = "ledOff.png"; // 즉시 반영
  database.ref('led').set({
    led: 0
  });
}

// LED 상태와 온도 데이터 변경 감지
database.ref('led').on('value', function(snapshot) {
  const val = snapshot.val();

  if (val && val.led === 0) {
    document.getElementById("img").src = "ledOff.png";
  } else {
    document.getElementById("img").src = "ledOn.png";
  }

  console.log(val);
});

// 온도 데이터 감지
database.ref('temperature').on('value', function(snapshot) {
  const val = snapshot.val();
  if (val) {
    document.getElementById("temperature").textContent =
      `현재 온도는 ${val.temp.toFixed(2)}도입니다.`;
  }
});

// Firebase 초기화 및 기타 코드 생략...

function sendMessage() {
  const chatInput = document.getElementById("chatInput");
  const message = chatInput.value.trim();

  if (message) {
    const chatbox = document.getElementById("chatbox");
    const messageElement = document.createElement("p");
    messageElement.textContent = message;
    chatbox.appendChild(messageElement);

    // 채팅창 스크롤을 제일 아래로 내림
    chatbox.scrollTop = chatbox.scrollHeight;

    // 입력 필드 초기화
    chatInput.value = '';
  }
}
