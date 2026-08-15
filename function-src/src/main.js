import { Client, TablesDB, Storage, Tokens } from "node-appwrite";

export default async ({ req, res, log, error }) => {
  try {
    const userId = req.headers["x-appwrite-user-id"];
    const apiKey = req.headers["x-appwrite-key"];

    if (!userId) {
      return res.json(
        { error: "Not authenticated" },
        401
      );
    }

    if (!apiKey) {
      error("Missing Appwrite dynamic API key");

      return res.json(
        { error: "Function authentication failed" },
        500
      );
    }

    const fileId = req.bodyJson?.fileId;

    if (!fileId) {
      return res.json(
        { error: "fileId is required" },
        400
      );
    }

    const client = new Client()
      .setEndpoint(process.env.APPWRITE_FUNCTION_API_ENDPOINT)
      .setProject(process.env.APPWRITE_FUNCTION_PROJECT_ID)
      .setKey(apiKey);

    const tablesDB = new TablesDB(client);
    const storage = new Storage(client);
    const tokens = new Tokens(client);

    const databaseId = process.env.DATABASE_ID;
    const tableId = process.env.TABLE_ID;
    const bucketId = process.env.BUCKET_ID;

    let row;

    try {
      row = await tablesDB.getRow({
        databaseId,
        tableId,
        rowId: fileId
      });
    } catch (e) {
      if (e.code === 404) {
        return res.json(
          { error: "File not found" },
          404
        );
      }

      throw e;
    }

    if (row.userId !== userId) {
      return res.json(
        {
          error: "You do not have permission to access this file"
        },
        403
      );
    }

   const wantsDownload = req.bodyJson?.download === true;

if (wantsDownload) {
  try {
    const expiresAt = new Date(
      Date.now() + 5 * 60 * 1000
    ).toISOString();

    const token = await tokens.createFileToken({
      bucketId,
      fileId: row.storageFileId,
      expire: expiresAt
    });

    const downloadUrl =
  `${process.env.APPWRITE_FUNCTION_API_ENDPOINT}/storage/buckets/` +
  `${bucketId}/files/${row.storageFileId}/download` +
  `?project=${encodeURIComponent(process.env.APPWRITE_FUNCTION_PROJECT_ID)}` +
  `&token=${encodeURIComponent(token.secret)}`;

    return res.json(
      {
        id: row.$id,
        fileName: row.filename,
        downloadUrl,
        expiresAt
      },
      200
    );
  } catch (e) {
    error(`File download authorization failed: ${e.message}`);

    return res.json(
      {
        error: "Could not create download link"
      },
      500
    );
  }
}

return res.json(
  {
    id: row.$id,
    ownerId: row.userId,
    fileName: row.filename,
    storageFileId: row.storageFileId
  },
  200
);

  } catch (e) {
    error(
      `File authorization failed: ${e.message}`
    );

    return res.json(
      {
        error: "Internal server error"
      },
      500
    );
  }
};
