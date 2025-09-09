Perfect ✅ I’ll give you a **single consolidated guide** that covers **both cases**: with persistence and without persistence. Each step has a short one-line explanation.

---

# 🐳 Run MongoDB in Podman

## 1. Install Podman

* **Windows:** Install [Podman Desktop](https://podman-desktop.io/) or via

  ```powershell
  winget install RedHat.Podman-Desktop
  ```
* **Linux (Ubuntu/Debian):**

  ```bash
  sudo apt update && sudo apt install podman -y
  ```

---

## 2. Verify Installation

```bash
podman --version
```

---

## 3. Pull MongoDB Image

```bash
podman pull docker.io/mongodb/mongodb-community-server:latest
```

---

## 4. Run MongoDB (Without Persistence 🚫)

* Data will be lost if the container is removed.

```bash
podman run -d --name todoDB -p 3000:27017 docker.io/mongodb/mongodb-community-server:latest
```

---

## 5. Run MongoDB (With Persistence ✅)

* Data is stored in a Podman volume (`mongo_data`).

```bash
podman run -d --name todoDB -p 3000:27017 -v mongo_data:/data/db docker.io/mongodb/mongodb-community-server:latest
```

---

## 6. Check Running Containers

```bash
podman ps
```

---

## 7. Connect to MongoDB

* From host (if `mongosh` installed):

  ```bash
  mongosh "mongodb://localhost:3000"
  ```
* Or directly inside container:

  ```bash
  podman exec -it todoDB mongosh
  ```

---

## 8. Test Database

```javascript
show dbs
use testdb
db.users.insertOne({ name: "Alice", age: 25 })
db.users.find()
```

---

## 9. Stop MongoDB Container

```bash
podman stop todoDB
```

---

## 10. Restart MongoDB Container

```bash
podman start todoDB
```

---

## 11. Remove Container

* If run **without persistence**, all data is lost.
* If run **with persistence**, data is preserved in volume.

```bash
podman rm todoDB
```

---

## 12. Remove Volume (⚠️ Deletes All Data)

```bash
podman volume rm mongo_data
```

---

👉 This way you can choose between **ephemeral MongoDB** (quick testing) or **persistent MongoDB** (real usage).

Do you want me to also prepare a **ready-to-save `.md` cheat sheet file** so you can drop it directly into GitHub/notes?
