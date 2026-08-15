const APPWRITE_ENDPOINT = "https://sgp.cloud.appwrite.io/v1";
const APPWRITE_PROJECT_ID = "6a80103a0039331a4b7e";
const APPWRITE_DATABASE_ID = "secure-login-db";
const APPWRITE_TABLE_ID = "files";
const APPWRITE_BUCKET_ID = "secure-login-files";

const appwriteClient = new Appwrite.Client()
  .setEndpoint(APPWRITE_ENDPOINT)
  .setProject(APPWRITE_PROJECT_ID);

const account = new Appwrite.Account(appwriteClient);
const tablesDB = new Appwrite.TablesDB(appwriteClient);
const storage = new Appwrite.Storage(appwriteClient);
window.appwriteStorage = storage;
const functions = new Appwrite.Functions(appwriteClient);

const realFetch = window.fetch.bind(window);

function appwriteJson(status, body) {
  return new Response(JSON.stringify(body), {
    status,
    headers: {
      "Content-Type": "application/json"
    }
  });
}

function isAppwriteMode() {
  const mode = document.querySelector(
    'input[name="backendMode"]:checked'
  );

  return mode && mode.value === "appwrite";
}

async function getCurrentUser() {
  try {
    return await account.get();
  } catch (error) {
    return null;
  }
}

async function handleRegister(req) {
  const { email, password } = await req.json();

  if (!email || !password) {
    return appwriteJson(400, {
      error: "email and password are required"
    });
  }

  try {
    const user = await account.create({
      userId: Appwrite.ID.unique(),
      email,
      password
    });

    return appwriteJson(201, {
      id: user.$id,
      email: user.email
    });
  } catch (error) {
    if (error.code === 409) {
      return appwriteJson(409, {
        error: "An account with that email already exists"
      });
    }

    return appwriteJson(
      error.code || 400,
      {
        error: error.message || "Registration failed"
      }
    );
  }
}

async function handleLogin(req) {
    try {
    const existingUser = await account.get();

    return appwriteJson(200, {
      message: "Already logged in",
      user: {
        id: existingUser.$id,
        email: existingUser.email
      }
    });
  } catch (error) {
    // No active session — continue with normal login.
  }
  const { email, password } = await req.json();

  if (!email || !password) {
    return appwriteJson(400, {
      error: "email and password are required"
    });
  }

  try {
    const session = await account.createEmailPasswordSession({
      email,
      password
    });

    const user = await account.get();

    return appwriteJson(200, {
      user: {
        id: user.$id,
        email: user.email
      },
      session: {
        id: session.$id
      }
    });
  } catch (error) {
    console.error("Appwrite login error:", error);

    return appwriteJson(401, {
      error: error.message || "Invalid email or password",
      type: error.type || "unknown",
      code: error.code || 401
    });
  }
}

async function handleLogout() {
  try {
    await account.deleteSession({
      sessionId: "current"
    });

    return appwriteJson(200, {
      message: "Logged out"
    });
  } catch (error) {
    return appwriteJson(401, {
      error: "Not authenticated"
    });
  }
}

async function handleMe() {
  try {
    const user = await account.get();

    return appwriteJson(200, {
      id: user.$id,
      email: user.email,
      profile: {
        fullName: user.name || "",
        displayName: user.name || user.email.split("@")[0],
        bio: "",
        createdAt: user.$createdAt,
        role: "user"
      }
    });
  } catch (error) {
    return appwriteJson(401, {
      error: "Not authenticated"
    });
  }
}

async function handleFiles() {
  try {
    const result = await tablesDB.listRows({
      databaseId: APPWRITE_DATABASE_ID,
      tableId: APPWRITE_TABLE_ID
    });

    const files = result.rows.map((row) => ({
      id: row.$id,
      ownerId: row.userId,
      fileName: row.filename,
      storageFileId: row.storageFileId
    }));

    return appwriteJson(200, {
      files
    });
  } catch (error) {
    if (error.code === 401 || error.code === 403) {
      return appwriteJson(401, {
        error: "Not authenticated"
      });
    }

    return appwriteJson(
      error.code || 500,
      {
        error: error.message || "Could not retrieve files"
      }
    );
  }
}

async function handleFileById(fileId) {
  try {
         const execution = await functions.createExecution({
         functionId: "6a804e2c002b3a972cda",
         body: JSON.stringify({ fileId }),
         async: false,
         path: "/",
         method: "POST" 
      });

    let body;

    try {
      body = JSON.parse(execution.responseBody);
    } catch {
      body = execution.responseBody;
    }

    return appwriteJson(
      execution.responseStatusCode || 500,
      body
    );
  } catch (error) {
    console.error("Function execution error:", error);

    return appwriteJson(500, {
      error: error.message || "Could not access file"
    });
  }
}

async function handleFileDownload(fileId) {
  try {
    const execution = await functions.createExecution({
      functionId: "6a804e2c002b3a972cda",
      body: JSON.stringify({
        fileId,
        download: true
      }),
      async: false,
      path: "/",
      method: "POST"
    });

    let body;

    try {
      body = JSON.parse(execution.responseBody);
    } catch {
      body = execution.responseBody;
    }

    return appwriteJson(
      execution.responseStatusCode || 500,
      body
    );

  } catch (error) {
    console.error("File download Function error:", error);

    return appwriteJson(500, {
      error: error.message || "Could not create download link"
    });
  }
}
window.fetch = async function(input, init = {}) {
  if (!isAppwriteMode()) {
    return realFetch(input, init);
  }

  const url =
    typeof input === "string"
      ? input
      : input.url;

  const parsedUrl = new URL(
    url,
    window.location.href
  );

  const pathname = parsedUrl.pathname;

  const req = new Request(
    url,
    init
  );

  if (
    pathname === "/register" &&
    req.method === "POST"
  ) {
    return handleRegister(req);
  }

  if (
    pathname === "/login" &&
    req.method === "POST"
  ) {
    return handleLogin(req);
  }

  if (
    pathname === "/logout" &&
    req.method === "POST"
  ) {
    return handleLogout();
  }

  if (
    pathname === "/me" &&
    req.method === "GET"
  ) {
    return handleMe();
  }

  if (
    pathname === "/files" &&
    req.method === "GET"
  ) {
    return handleFiles();
  }

  const downloadMatch =
    pathname.match(
      /^\/files\/([^/]+)\/download$/
    );

  if (
    downloadMatch &&
    req.method === "GET"
  ) {
    return handleFileDownload(
      downloadMatch[1]
    );
  }

  const fileMatch =
    pathname.match(
      /^\/files\/([^/]+)$/
    );

  if (
    fileMatch &&
    req.method === "GET"
  ) {
    return handleFileById(
      fileMatch[1]
    );
  }

  return realFetch(input, init);
};

console.info(
  "[appwrite-adapter] Appwrite adapter loaded"
);
