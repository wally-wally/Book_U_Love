import Vue from "vue";
import Vuex from "vuex";
import user from "./modules/user.js";
import data from "./modules/data.js";
import common from "./modules/common.js";

Vue.use(Vuex);

export default new Vuex.Store({
  modules: {
    common,
    user,
    data
  }
});
