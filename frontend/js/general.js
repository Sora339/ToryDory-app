const checkLogin = () => {
  if (localStorage.getItem("token")) {
    return true;
  }
  return false;
};

const gettoday = () => {
  const today = new Date();
  const year = today.getFullYear();
  const month = (today.getMonth() + 1).toString().padStart(2, "0");
  const date = (today.getDate()).toString().padStart(2, "0");
  const fulldate = year + "-" + month + "-" + date;
  return fulldate;
};

//時計を設置
const setClock = () => {
  const clock1 = document.getElementById("clock1");
  const clock2 = document.getElementById("clock2");
  const date = new Date();
  const fulldate = gettoday();
  const hours = date.getHours();
  const minutes = date.getMinutes().toString().padStart(2, "0");
  clock1.innerHTML = `${fulldate} ${hours}:${minutes}`;
  clock2.innerHTML = `${fulldate}`;
};
