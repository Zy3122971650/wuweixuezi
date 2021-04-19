<template>
  <div>
    <div class="login">
      <el-tabs v-model="activeName">
        <el-tab-pane
          label="手机号登录"
          name="first"
        >
          <el-input
            v-model="phone_number"
            placeholder="手机号"
          ></el-input>
          <el-input
            v-model="passwd"
            placeholder="密码"
            type="password"
          ></el-input>

          <el-button
            @click="submit()"
            round
          >提交</el-button>
        </el-tab-pane>
        <el-tab-pane
          label="身份证登录"
          name="second"
        >
          <el-input
            v-model="id_card"
            placeholder="身份证号码"
          ></el-input>
          <el-input
            v-model="passwd"
            placeholder="密码"
            type="password"
          ></el-input>
          <el-select
            v-model="school_code"
            placeholder="选择学校"
          >
            <el-option
              v-for="item in options"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            >
            </el-option>
          </el-select>
          <el-button
            @click="submit()"
            round
          >提交</el-button>
        </el-tab-pane>
      </el-tabs>
    </div>
    <article style="color:red">
      <h2>注意事项</h2>
      <p>程序通过模拟登录完成签到和领水的操作，所以当您登录五维学子发现账号在别处登录属于正常现象</p>
      <p>为了避免僵尸账户抢占数据库和计算资源，每年9月1日将会清空数据库，届时您需要重新在本页面录入数据</p>
    </article>
    <article>
      <h2>声明</h2>
      <p>本网站，仅供内部使用，禁止任何公众号、自媒体进行任何形式的转载、发布。</p>
      <p>本网站背后使用的是由开源社区提供的脚本，如果任何单位或个人认为该网站可能涉嫌侵犯其权利，则应及时通知并提供身份证明，所有权证明，我们将在收到认证文件后关闭网站.</p>
    </article>
  </div>
</template>

<script>
import axios from "axios";
import { ElMessage } from "element-plus";
export default {
  data() {
    const options = [
      {
        value: "7",
        label: "大连工业大学",
      },
      {
        value: "8",
        label: "辽宁对外经贸学院",
      },
      {
        value: "9",
        label: "辽东学院",
      },
      {
        value: "10",
        label: "辽工大_葫芦岛",
      },
      {
        value: "11",
        label: "大连技师学院",
      },
      {
        value: "12",
        label: "东北财经大学",
      },
      {
        value: "13",
        label: "辽宁师范大学",
      },
      {
        value: "14",
        label: "大连航运职业技术学院",
      },
    ];
    return {
      activeName: "first",
      phone_number: "",
      passwd: "",
      id_card: "",
      school_code: "",
      chosen_date: "",
      error: 0,
      rightShow: 0,
      options,
      school: "",
    };
  },
  methods: {
    submit() {
      let chosen_mode;
      if (this.activeName == "first") {
        chosen_mode = 3;
      } else {
        chosen_mode = 1;
      }
      const user_info = {
        id_number: this.id_card,
        phone_number: this.phone_number,
        password: this.passwd,
        school_code: this.school_code,
        style: chosen_mode,
      };

      axios.post("/api/save", { data: user_info }).then((response) => {
        const code = response.data["code"];
        if (code == "0") {
          ElMessage.success({
            message: response.data["messg"],
            type: "success",
          });
        } else if (code == "1") {
          ElMessage.error({
            message: response.data["messg"],
            type: "error",
          });
        } else {
          ElMessage.warning({
            message: response.data["messg"],
            type: "warning",
          });
        }
      });
    },
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
.login {
  margin-top: 60px;
  height: 300px;
  width: 300px;
  margin: 200px auto;
}
</style>
