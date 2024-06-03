const API_HOST = "http://localhost:8000";

const logout = () => {
  localStorage.removeItem("token");
  location.href = "/login.html";
};

const handleLoginError = () => {
  alert("ログイン情報が確認できませんでした、ログインページに移動します");
  logout();
};

const handleForbiddenError = () => {
  alert("他のユーザーのタスクは閲覧できません");
  throw new Error("他のユーザーのタスクは閲覧できません");
};

const handleOtherError = () => {
  alert("予期せむエラーが発生しました");
  throw new Error("予期せむエラーが発生しました");
};

/**
 * ユーザー新規登録API
 */
const signUpApi = (data) => {
  const url = `${API_HOST}/user`;
  return fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  }).then((res) => {
    if (res.ok) {
      return res.json();
    } else if (res.status === 400) {
      console.error(res);
      throw new Error("入力されたメールアドレスは既に登録されています");
    } else {
      console.error(res);
      handleOtherError();
    }
  });
};

/**
 * ログインAPI
 */
const loginApi = (email, password) => {
  const url = `${API_HOST}/token`;
  return fetch(url, {
    method: "POST",
    credentials: "include",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    // loginの場合のみ、bodyは特別
    body: `username=${email}&password=${password}`,
  })
    .then((res) => {
      if (res.ok) {
        return res.json();
      } else if (res.status === 401) {
        console.error(res);
        throw new Error("メールアドレスまたはパスワードが間違っています");
      } else {
        console.error(res);
        handleOtherError();
      }
    })
    .then((data) => {
      localStorage.setItem("token", data.access_token);
      return data;
    });
};

/**
 * アイコンの画像を更新するAPI
 */
const updateiconImageApi = (myId, file) => {
  const url = `${API_HOST}/user/${myId}/image`;
  const formData = new FormData();
  formData.append("icon_img_path", file);
  console.log(formData);
  return fetch(url, {
    method: "PUT",
    headers: {
      Authorization: `Bearer ${localStorage.getItem("token")}`,
    },
    body: formData,
  }).then((res) => {
    if (res.ok) {
      return res.json();
    } else if (res.status === 401) {
      handleLoginError();
    } else if (res.status === 403) {
      handleForbiddenError();
    } else {
      console.error(res);
      handleOtherError();
    }
  });
};

/**
 * ログインユーザー情報取得するAPI
 */
const getMeApi = () => {
  const url = `${API_HOST}/me`;
  return fetch(url, {
    method: "GET",
    headers: {
      Authorization: `Bearer ${localStorage.getItem("token")}`,
    },
  }).then((res) => {
    if (res.ok) {
      return res.json();
    } else if (res.status === 401) {
      handleLoginError();
    } else {
      console.error(res);
      handleOtherError();
    }
  });
};

/**
 * 全てのタスク取得するAPI
 */
const getAllTasksApi = () => {
  const url = `${API_HOST}/tasks`;
  return fetch(url, {
    method: "GET",
    headers: {
      Authorization: `Bearer ${localStorage.getItem("token")}`,
    },
  }).then((res) => {
    if (res.ok) {
      return res.json();
    } else if (res.status === 401) {
      handleLoginError();
    } else {
      console.error(res);
      handleOtherError();
    }
  });
};

/**
 * タスクを完了にするAPI
 */
const doneTaskApi = (taskId, doneDate) => {
  const url = `${API_HOST}/task/${taskId}/done`;
  const body = {
    done_date: doneDate,
  };
  return fetch(url, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${localStorage.getItem("token")}`,
    },
    body: JSON.stringify(body),
  })
    .then((res) => {
      if (res.ok) {
        return res.json();
      } else if (res.status === 401) {
        handleLoginError();
      } else {
        console.error(res);
        handleOtherError();
      }
    })
    .catch((error) => {
      console.error("Error:", error);
    });
};

/**
 * タスクを実行中にするAPI
 */
const doingTaskApi = (taskId) => {
  const url = `${API_HOST}/task/${taskId}/doing`;
  return fetch(url, {
    method: "PUT",
    headers: {
      Authorization: `Bearer ${localStorage.getItem("token")}`,
    },
  }).then((res) => {
    if (res.ok) {
      return res.json();
    } else if (res.status === 401) {
      handleLoginError();
    } else {
      console.error(res);
      handleOtherError();
    }
  });
};

/**
 * タスクを未完了にするAPI
 */
const undoneTaskApi = (taskId) => {
  const url = `${API_HOST}/task/${taskId}/done`;
  return fetch(url, {
    method: "DELETE",
    headers: {
      Authorization: `Bearer ${localStorage.getItem("token")}`,
    },
  }).then((res) => {
    if (res.ok) {
      return res.json();
    } else if (res.status === 401) {
      handleLoginError();
    } else {
      console.error(res);
      handleOtherError();
    }
  });
};

/**
 * タスクを実行中から未完了にするAPI
 */
const undoingTaskApi = (taskId) => {
  const url = `${API_HOST}/task/${taskId}/doing`;
  return fetch(url, {
    method: "DELETE",
    headers: {
      Authorization: `Bearer ${localStorage.getItem("token")}`,
    },
  }).then((res) => {
    if (res.ok) {
      return res.json();
    } else if (res.status === 401) {
      handleLoginError();
    } else {
      console.error(res);
      handleOtherError();
    }
  });
};

/**
 * ひとつのタスクを取得するAPI
 */
const getTaskDetailApi = (taskId) => {
  const url = `${API_HOST}/task/${taskId}`;
  return fetch(url, {
    method: "GET",
    headers: {
      Authorization: `Bearer ${localStorage.getItem("token")}`,
    },
  }).then((res) => {
    if (res.ok) {
      return res.json();
    } else if (res.status === 401) {
      handleLoginError();
    } else if (res.status === 403) {
      handleForbiddenError();
    } else {
      console.error(res);
      handleOtherError();
    }
  });
};

/**
 * タスクを作成するAPI
 */
const createTaskApi = (data) => {
  console.log("作成実行！");
  const url = `${API_HOST}/task`;
  return fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${localStorage.getItem("token")}`,
    },
    body: JSON.stringify(data),
  }).then((res) => {
    if (res.ok) {
      return res.json();
    } else if (res.status === 401) {
      handleLoginError();
    } else {
      console.error(res);
      handleOtherError();
    }
  });
};

/**
 * タスクを更新するAPI
 */
const updateTaskApi = (taskId, data) => {
  const url = `${API_HOST}/task/${taskId}`;
  return fetch(url, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${localStorage.getItem("token")}`,
    },
    body: JSON.stringify(data),
  }).then((res) => {
    if (res.ok) {
      return res.json();
    } else if (res.status === 401) {
      handleLoginError();
    } else if (res.status === 403) {
      handleForbiddenError();
    } else {
      console.error(res);
      handleOtherError();
    }
  });
};

/**
 * タスクの画像を更新するAPI
 */
const updateTaskImageApi = (taskId, file) => {
  const url = `${API_HOST}/task/${taskId}/image`;
  const formData = new FormData();
  formData.append("image", file);
  return fetch(url, {
    method: "PUT",
    headers: {
      Authorization: `Bearer ${localStorage.getItem("token")}`,
    },
    body: formData,
  }).then((res) => {
    if (res.ok) {
      return res.json();
    } else if (res.status === 401) {
      handleLoginError();
    } else if (res.status === 403) {
      handleForbiddenError();
    } else {
      console.error(res);
      handleOtherError();
    }
  });
};

/**
 * タスクを削除するAPI
 */
const deleteTaskApi = (taskId) => {
  const url = `${API_HOST}/task/${taskId}`;
  return fetch(url, {
    method: "DELETE",
    headers: {
      Authorization: `Bearer ${localStorage.getItem("token")}`,
    },
  }).then((res) => {
    if (res.ok) {
      return res.json();
    } else if (res.status === 401) {
      handleLoginError();
    } else if (res.status === 403) {
      handleForbiddenError();
    } else {
      console.error(res);
      handleOtherError();
    }
  });
};

//完了タスクの一覧を取得する
const getDonetaskApi = () => {
  const url = `${API_HOST}/donetask`;
  return fetch(url, {
    method: "GET",
    headers: {
      Authorization: `Bearer ${localStorage.getItem("token")}`,
    },
  }).then((res) => {
    if (res.ok) {
      return res.json();
    } else if (res.status === 401) {
      handleLoginError();
    } else {
      console.error(res);
      handleOtherError();
    }
  });
};

/**
 * 日記を作成するAPI
 */
const createDiaryApi = (data) => {
  const url = `${API_HOST}/diary`
  return fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${localStorage.getItem('token')}`,
    },
    body: JSON.stringify(data),
  }).then((res) => {
    if (res.ok) {
      return res.json()
    } else if (res.status === 401) {
      handleLoginError()
    } else {
      console.error(res)
      handleOtherError()
    }
  })
}

/**
 * アイコンの画像を更新するAPI
 */

const updateDiaryImageApi = (diaryId, file) => {
  const url = `${API_HOST}/diary/${diaryId}/image`;
  const formData = new FormData();
  formData.append("diary_img_path", file); // キー名がAPIで期待されているものと一致していることを確認
  console.log(formData);
  return fetch(url, {
    method: "PUT",
    headers: {
      Authorization: `Bearer ${localStorage.getItem("token")}`,
    },
    body: formData,
  }).then((res) => {
    if (res.ok) {
      return res.json();
    } else if (res.status === 401) {
      handleLoginError();
    } else if (res.status === 403) {
      handleForbiddenError();
    } else {
      console.error(res);
      handleOtherError();
    }
  }).catch((error) => {
    console.error("Fetch error:", error);
  });
};

//日記一覧を取得

const getAlldiaryApi = () => {
  const url = `${API_HOST}/diarys`;
  return fetch(url, {
    method: "GET",
    headers: {
      Authorization: `Bearer ${localStorage.getItem("token")}`,
    },
  }).then((res) => {
    if (res.ok) {
      return res.json();
    } else if (res.status === 401) {
      handleLoginError();
    } else {
      console.error(res);
      handleOtherError();
    }
  });
};
