<template>
  <div class="comment-management">
    <h2>评论管理</h2>
    <div class="table-container">
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>用户名</th>
            <th>评论内容</th>
            <th>时间</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="comment in comments" :key="comment.id">
            <td>{{ comment.id }}</td>
            <td>{{ comment.commenter_name || "匿名用户" }}</td>
            <td>{{ comment.content }}</td>
            <td>{{ formatDate(comment.create_time) }}</td>
            <td><button @click="deleteComment(comment.id)">删除</button></td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      comments: [],
      token: sessionStorage.getItem("token"), // 获取存储的 token
    };
  },
  created() {
    this.fetchComments();
  },
  methods: {
    // 获取评论列表
    async fetchComments() {
      try {
        const response = await axios.get(
          "http://127.0.0.1:8000/user/manage_comments/",
          {
            headers: {
              Authorization: `Bearer ${this.token}`, // 携带 token
            },
          }
        );
        this.comments = response.data.comments;
      } catch (error) {
        console.error("获取评论失败:", error);
      }
    },

    // 删除评论
    async deleteComment(id) {
      if (confirm("确定删除此评论？")) {
        try {
          await axios.delete("http://127.0.0.1:8000/user/manage_comments/", {
            headers: {
              Authorization: `Bearer ${this.token}`, // 携带 token
            },
            data: { id },
          });
          this.fetchComments(); // 重新获取评论列表
        } catch (error) {
          console.error("删除评论失败:", error);
        }
      }
    },

    // 格式化时间
    formatDate(dateString) {
      const date = new Date(dateString);
      return date.toLocaleString(); // 可自定义日期格式
    },
  },
};
</script>

<style scoped>
.comment-management {
  padding: 30px;
  background-color: #f4f6f9;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

h2 {
  font-size: 24px;
  margin-bottom: 20px;
  color: #333;
}

.table-container {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

th,
td {
  padding: 12px 15px;
  text-align: left;
  font-size: 16px;
  color: #666;
  border-bottom: 1px solid #f1f1f1;
}

th {
  background-color: #f8f8f8;
  font-weight: 600;
  color: #333;
}

td {
  background-color: #fff;
}

button {
  padding: 6px 12px;
  background-color: #ff4f5a;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

button:hover {
  background-color: #e04b53;
}

button:focus {
  outline: none;
}

@media (max-width: 768px) {
  table {
    font-size: 14px;
  }

  th,
  td {
    padding: 10px;
  }
}
</style>
