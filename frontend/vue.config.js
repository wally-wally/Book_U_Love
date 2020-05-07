module.exports = {
  publicPath: "/",
  devServer: {
    proxy: {
      "/api": {
        target: "http://i02b205.p.ssafy.io/:8000/"
      }
    }
  },
  transpileDependencies: ["vuetify"]
};
