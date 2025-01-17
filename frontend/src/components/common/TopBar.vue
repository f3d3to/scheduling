<template>
  <div class="topbar">
    <div class="container">
      <div class="app-name">
        <router-link to="/">
          <img src="@/assets/icon-fill.png" alt="Logo" class="logo" />
          <h3>ESTUDI-AR</h3>
        </router-link>
      </div>
      <div class="search-bar">
        <input type="text" placeholder="Filtrar..." />
      </div>
      <div class="user-actions">
        <div v-if="isLoggedIn" class="user-info">
          <span class="username">{{ userName }}</span>
          <v-menu v-model="showDropdown" location="bottom" :close-on-content-click="false" offset-y>
            <template v-slot:activator="{ props }">
              <v-btn icon v-bind="props" class="profile-icon">
                <v-icon>mdi-account-circle</v-icon>
              </v-btn>
            </template>
            <v-list density="compact" class="dropdown-menu">

              <v-list-item to="/mi-perfil">
                <v-icon>mdi-account</v-icon> Ver Perfil

              </v-list-item>
              <v-list-item @click="logout">
                <v-icon>mdi-logout</v-icon> Cerrar Sesión
              </v-list-item>
            </v-list>
          </v-menu>
        </div>
        <template v-else>
          <router-link to="/iniciar-sesion" class="login-icon">
            <v-icon>mdi-login</v-icon> Iniciar Sesión
          </router-link>
          <router-link to="/registro" class="register-link">
            Registrarse
          </router-link>
        </template>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "TopBar",
  data() {
    return {
      showDropdown: false,
      isLoggedIn: true,
      userName: "username",
    };
  },
  methods: {
    toggleDropdown() {
      this.showDropdown = !this.showDropdown;
    },
    logout() {
      console.log("debería desloguear");
    },
  },
};
</script>
<style scoped>
/* Importamos la fuente de MDI aquí (si ya la tienes instalada globalmente, puedes omitir esto) */

.topbar {
  background: linear-gradient(90deg, #2c2c3e, #1e1e2f);
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
  color: white;
}

.container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
  height: 60px;
  max-width: 1200px;
  margin: 0 auto;
}

.app-name {
  display: flex;
  align-items: center;
  font-size: 1.5rem;
  font-weight: bold;
}

.app-name h1 {
  margin: 0 0 0 10px; /* Añadimos un margen a la izquierda del h1 */
}

.app-name a {
  text-decoration: none;
  color: inherit;
  display: flex; /* Para que el logo y el h1 estén en línea */
  align-items: center; /* Para alinear verticalmente el logo y el h1 */
}

.logo {
  height: 40px; /* Ajusta el tamaño del logo según tus necesidades */
  margin-right: 10px; /* Espacio entre el logo y el texto */
}

.search-bar {
  flex-grow: 1;
  margin: 0 20px;
  max-width: 400px;
}

.search-bar input {
  width: 100%;
  padding: 10px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 5px;
  background-color: #1e1e2f;
  color: #fff;
  font-size: 1rem;
  outline: none;
  transition: border-color 0.3s ease;
}

.search-bar input::placeholder {
  color: rgba(255, 255, 255, 0.5);
}

.search-bar input:focus {
  border-color: #535bf2;
}

.user-actions {
  display: flex;
  align-items: center;
}

.user-info {
  display: flex;
  align-items: center;
}

.username {
  margin-right: 10px;
  font-weight: bold;
}

.profile-icon {
  background: none;
  border: none;
  padding: 0;
  cursor: pointer;
  font-size: 1.5rem;
  color: white;
  margin-right: 20px;
}
.login-icon,
.register-link {
  display: flex;
  align-items: center;
  color: white;
  text-decoration: none;
  margin-left: 15px;
  padding: 5px 10px;
  transition: background-color 0.3s ease;
}

.login-icon i,
.register-link i {
  margin-right: 5px;
}

.login-icon:hover,
.register-link:hover {
  background-color: #2c2c3e;
}
</style>