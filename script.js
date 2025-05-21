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
  database.ref('led').set({
    led: 1
  });
}

function ledOFF() {
  console.log("LED OFF");
  database.ref('led').set({
    led: 0
  });
}

// 데이터 변경 감지
database.ref('led').on('value', function(snapshot) {
  const val = snapshot.val();
  
  if (val && val.led === 0) {
    document.getElementById("img").src = "ledOff.png";
  } else {
    document.getElementById("img").src = "ledOn.png";
  }
  
  console.log(val);
});
