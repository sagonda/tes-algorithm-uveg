# 🔐 Generando Token Personal de GitHub

## Paso 1: Crear el Token en GitHub

1. Abre: https://github.com/settings/tokens/new
   (O ve a Settings → Developer settings → Personal access tokens → Tokens (classic))

2. Configura el token:
   - **Name**: `tes-algorithm-uveg-push`
   - **Expiration**: `90 days` (o según prefieras)
   - **Scopes necesarios**: Marca estas casillas:
     - ✅ `repo` (acceso completo a repositorios)
     - ✅ `write:repo_hook` (webhooks)
     - ✅ `read:user` (información de usuario)

3. Haz click en **"Generate token"**

4. **COPIA EL TOKEN** (verás un string similar a este):
   ```
   ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

   ⚠️ **IMPORTANTE**: Solo verás el token UNA VEZ. Si lo pierdes, deberás generar otro.

## Paso 2: Usar el Token para hacer Push

Cuando Git pida credenciales:

```
Username for 'https://github.com': sagonda
Password for 'https://sagonda@github.com': [PEGA TU TOKEN AQUÍ]
```

**Nota**: La contraseña es el TOKEN, no tu contraseña de GitHub.

## Paso 3: Guardar Credenciales (Opcional)

Si respondiste `s` a guardar credenciales, Git almacenará el token en:
```
~/.git-credentials
```

Así no tendrás que ingresarlo cada vez.

## ⚠️ SEGURIDAD

- Nunca compartas tu token
- Nunca lo commits en repositorios
- Si lo expones accidentalmente, revócalo desde:
  https://github.com/settings/tokens

---

**¿Ya tienes tu token?** Ejecuta entonces:
```bash
cd /home/sagonda/Documentos/git/projects/TES_ALGORITHM_UVEG
git push -u origin main
```

Verás que pide:
- Username: `sagonda`
- Password: [Tu token personal]

Pegalo y presiona Enter.
