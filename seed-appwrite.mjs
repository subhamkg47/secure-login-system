import dotenv from "dotenv";
import * as sdk from "node-appwrite";
import { InputFile } from "node-appwrite/file";

dotenv.config({ path: ".env.appwrite" });
import path from "path";
import { fileURLToPath } from "url";

const {
  APPWRITE_ENDPOINT,
  APPWRITE_PROJECT_ID,
  APPWRITE_API_KEY,
  APPWRITE_DATABASE_ID,
  APPWRITE_TABLE_ID,
  APPWRITE_BUCKET_ID,
} = process.env;

if (
  !APPWRITE_ENDPOINT ||
  !APPWRITE_PROJECT_ID ||
  !APPWRITE_API_KEY ||
  !APPWRITE_DATABASE_ID ||
  !APPWRITE_TABLE_ID ||
  !APPWRITE_BUCKET_ID
) {
  throw new Error("Missing Appwrite environment variables");
}

const client = new sdk.Client()
  .setEndpoint(APPWRITE_ENDPOINT)
  .setProject(APPWRITE_PROJECT_ID)
  .setKey(APPWRITE_API_KEY);

const storage = new sdk.Storage(client);
const tablesDB = new sdk.TablesDB(client);

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const uploadDir = path.join(__dirname, "backend", "uploads");

const users = {
  "securitytest@gmail.com": {
    id: "6a80206000273e18e7b4",
    files: [
      {
        id: "file_001",
        filename: "resume.pdf",
      },
      {
        id: "file_002",
        filename: "project.pdf",
      },
    ],
  },

  "user2@example.com": {
    id: "6a8020cf001ca6d928bf",
    files: [
      {
        id: "file_003",
        filename: "notes.pdf",
      },
      {
        id: "file_004",
        filename: "assignment.pdf",
      },
    ],
  },

  "user3@example.com": {
    id: "6a8021000019b9778a5c",
    files: [
      {
        id: "file_005",
        filename: "certificate.pdf",
      },
      {
        id: "file_006",
        filename: "project.zip",
      },
    ],
  },
};

async function seedFile(userId, file) {
  const localPath = path.join(uploadDir, file.filename);

  console.log(`\nUploading ${file.filename}...`);

  try {
    await storage.createFile({
      bucketId: APPWRITE_BUCKET_ID,
      fileId: file.id,
      file: InputFile.fromPath(localPath, file.filename),
      permissions: [
        sdk.Permission.read(sdk.Role.user(userId)),
      ],
    });

    console.log(`Uploaded: ${file.filename}`);
  } catch (error) {
    if (error.code === 409) {
      console.log(`Already exists: ${file.filename}`);
    } else {
      throw error;
    }
  }

  console.log(`Creating database row for ${file.filename}...`);

  try {
    await tablesDB.upsertRow({
      databaseId: APPWRITE_DATABASE_ID,
      tableId: APPWRITE_TABLE_ID,
      rowId: file.id,
      data: {
        userId: userId,
        filename: file.filename,
        storageFileId: file.id,
      },
      permissions: [
        sdk.Permission.read(sdk.Role.user(userId)),
      ],
    });

    console.log(`Database row created: ${file.id}`);
  } catch (error) {
    if (error.code === 409) {
      console.log(`Database row already exists: ${file.id}`);
    } else {
      throw error;
    }
  }
}

async function main() {
  console.log("Starting Appwrite seed...");
  console.log(`Endpoint: ${APPWRITE_ENDPOINT}`);
  console.log(`Project: ${APPWRITE_PROJECT_ID}`);

  for (const [email, user] of Object.entries(users)) {
    console.log(`\n====================================`);
    console.log(`User: ${email}`);
    console.log(`Appwrite ID: ${user.id}`);
    console.log(`====================================`);

    for (const file of user.files) {
      await seedFile(user.id, file);
    }
  }

  console.log("\n====================================");
  console.log("Appwrite seed completed successfully!");
  console.log("6 files + 6 database rows processed.");
  console.log("====================================");
}

main().catch((error) => {
  console.error("\nSeed failed:");
  console.error(error);
  process.exit(1);
});
