function loadView(view) {
  return () => import (`@/views/${view}`)
}

function loadComponent(dirName, component) {
  return () => import (`@/components/${dirName}/${component}`)
}

export { loadView, loadComponent }