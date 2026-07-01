<template>
  <div>
    <el-table
        :data="tableData"
        border
        :height="tableHeight"
        stripe
        @row-click="handleRowClick"
        :row-class-name="tableRowClassName"
    >
      <el-table-column prop="id" label="ID" width="80"></el-table-column>
      <el-table-column prop="username" label="用户名" width="120"></el-table-column>
      <el-table-column prop="email" label="邮箱" width="180"></el-table-column>
      <el-table-column prop="phonenumber" label="手机号" width="120"></el-table-column>
      <el-table-column prop="status" label="状态" width="80">
        <template slot-scope="scope">
          <el-switch
              v-model="scope.row.status"
              active-value="1"
              inactive-value="0"
              @change="statusChangeHandle(scope.row)"
          ></el-switch>
        </template>
      </el-table-column>
      <el-table-column label="操作" :width="operationColWidth">
        <template slot-scope="scope">
          <el-button size="mini" @click="handleRoleDialogValue(scope.row.id, scope.row.roles)">分配角色</el-button>
          <el-button size="mini" type="warning" @click="confirmResetPassword(scope.row.id)">重置密码</el-button>
          <el-button size="mini" type="danger" @click="confirmDelete(scope.row.id)">删除</el-button>
          <el-button size="mini" type="primary" @click="handleDialogValue(scope.row.id)">编辑</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-pagination
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="queryForm.pageNum"
        :page-sizes="[10, 20, 30, 40]"
        :page-size="queryForm.pageSize"
        layout="total, sizes, prev, pager, next, jumper"
        :total="total"
    ></el-pagination>
    <el-dialog
        title="编辑用户信息"
        :visible.sync="dialogVisible"
        width="500px"
    >
      <el-form ref="editFormRef" :model="editForm" label-width="80px">
        <el-form-item label="用户名">
          <el-input v-model="editForm.username" disabled />
        </el-form-item>
        <el-form-item label="邮箱">
          <el-input v-model="editForm.email" />
        </el-form-item>
        <el-form-item label="手机号">
          <el-input v-model="editForm.phonenumber" />
        </el-form-item>
        <el-form-item label="备注">
          <el-input v-model="editForm.remark" type="textarea" />
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitEditUser">保存</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import requestUtil, { getServerUrl } from "@/util/request";

export default {
  data() {
    return {
      dialogVisible: false,
      editForm: {
        id: null,
        username: "",
        email: "",
        phonenumber: "",
        remark: "",
      },
      tableData: [],
      total: 0,
      queryForm: {
        query: "",
        pageNum: 1,
        pageSize: 10,
      },
      loading: false,
      tableHeight: 600,
      operationColWidth: 200,
    };
  },
  mounted() {
    this.initUserList();
    this.calculateTableHeight();
    window.addEventListener("resize", this.calculateTableHeight);
  },
  beforeDestroy() {
    window.removeEventListener("resize", this.calculateTableHeight);
  },
  methods: {
    async initUserList() {
      this.loading = true;
      try {
        const res = await requestUtil.post("user/search/", this.queryForm);
        this.tableData = res.data.userList;
        this.total = res.data.total;
      } catch (error) {
        console.error(error);
      } finally {
        this.loading = false;
      }
    },
    handleSizeChange(pageSize) {
      this.queryForm.pageNum = 1;
      this.queryForm.pageSize = pageSize;
      this.initUserList();
    },
    handleCurrentChange(pageNum) {
      this.queryForm.pageNum = pageNum;
      this.initUserList();
    },
    confirmResetPassword(id) {
      this.$confirm("确定要重置密码吗？", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      })
          .then(() => this.handleResetPassword(id))
          .catch(() => {
          });
    },
    confirmDelete(id) {
      this.$confirm("确定要删除该用户吗？", "警告", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "error",
      })
          .then(() => this.handleDelete(id))
          .catch(() => {
          });
    },
    calculateTableHeight() {
      const windowHeight = window.innerHeight;
      this.tableHeight = windowHeight - 320;
      this.operationColWidth = window.innerWidth < 768 ? 180 : 220;
    },
    getServerUrl() {
      return getServerUrl();
    },
    async statusChangeHandle(row) {
      try {
        await requestUtil.post(`user/status/${row.id}/${row.status}/`);
        this.$message.success("状态更新成功");
      } catch (error) {
        row.status = row.status === 1 ? 0 : 1;
        this.$message.error("状态更新失败");
      }
    },
    async handleResetPassword(id) {
      try {
        await requestUtil.post(`user/resetPwd/${id}/`);
        this.$message.success("密码已重置为默认值");
      } catch (error) {
        this.$message.error("重置密码失败");
      }
    },
    handleRoleDialogValue(id, roles) {
      // 实现角色分配对话框逻辑
      console.log("分配角色", id, roles);
    },
    handleDialogValue(id) {
      const user = this.tableData.find((user) => user.id === id);
      if (!user) {
        this.$message.error("未找到用户信息");
        return;
      }

      //  复制数据到 `editForm`
      this.editForm = {...user};

      // 显示编辑对话框
      this.dialogVisible = true;
    },
    async submitEditUser() {
      try {
        const response = await requestUtil.post("user/save/", this.editForm);
        if (response.data.code === 200) {
          this.$message.success("用户信息更新成功");
          this.dialogVisible = false; // 关闭对话框
          this.initUserList(); // 重新加载用户列表
        } else {
          this.$message.error("更新失败：" + response.data.msg);
        }
      } catch (error) {
        console.error("更新用户信息失败", error);
        this.$message.error("更新失败");
      }
    },
    async handleDelete(id) {
      try {
        await requestUtil.post(`http://127.0.0.1:8000/user/delete/${id}/`);
        this.$message.success("删除成功");
        this.initUserList();
      } catch (error) {
        this.$message.error("删除失败");
      }
    },
  },
};
</script>

<style lang="scss" scoped>
/* 原有样式 */
</style>