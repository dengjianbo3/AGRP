import { showToast } from "@/app/components/ui-lib";
import { createMessage, ExtendedChatMessage , MultimodalContent} from "@/app/store";
import { nanoid } from "nanoid";
import { API_BASE_URL } from "@/app/constant";
import { base64Image2Blob,} from "@/app/utils/chat";

export async function uploadFileToServer(
  file: File, 
  chatStore: any,
  dbName: string,
  chunkSize: string,
  chunkOverlap: string
): Promise<void> {
  const fileExt = file.name.split(".").pop()?.toLowerCase();
  if (!fileExt) {
    console.log("Unsupported file type");
    return;
  }

  const formData = new FormData();
  formData.append("file", file);

  try {
    let url = "";
    if (["csv", "xlsx", "xls"].includes(fileExt)) {
      url = `${API_BASE_URL}/upload_file/upload_excel_or_csv`;
    } else if (["pdf", "doc", "docx", "png", "jpg", "jpeg"].includes(fileExt)) {
      url = `${API_BASE_URL}/upload_file/upload_doc`;
      formData.append("db_name", dbName); 
      formData.append("chunk_size", chunkSize); 
      formData.append("chunk_overlap", chunkOverlap); 
      formData.append("files", file); 
    } else {
      console.log("Unsupported file type");
      return;
    }

    const response = await fetch(url, {
      method: "POST",
      body: formData,
    });

    if (response.ok) {
      showToast(`文件上传成功: ${file.name}`);
      const responseMessage = createMessage({
        role: 'assistant',
        content: `文件上传成功: ${file.name}`,
        date: new Date().toISOString(),
        id: nanoid(),
      });
      chatStore.addMessage(responseMessage);
    } else {
      const errorDetail = await response.json();
      showToast(`文件上传失败: ${file.name} - ${errorDetail.detail}`);
    }
  } catch (error) {
    console.error(`Error uploading file: ${file.name}`, error);
    showToast(`文件上传出错: ${file.name}`);
    const responseMessage = createMessage({
      role: 'assistant',
      content: `文件上传出错: ${file.name}`,
      date: new Date().toISOString(),
      id: nanoid(),
    });
    chatStore.addMessage(responseMessage);
  }
}

export async function sendQueryToServer(
  userInput: string,
  chatStore: any,
  dbName: string,
  tableFileName: string,
  docFileName: string
) {
  try {
    const url = `${API_BASE_URL}/query`;
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: new URLSearchParams({
        query: userInput,
        db_name: dbName,
        table_file_name: tableFileName,
        doc_file_name: docFileName,
      }),
    });

    if (!response.ok) {
      throw new Error('Network response was not ok: ' + response.statusText);
    }

    const data = await response.json();
    const responseMessageContent = data.answer || "No response";

    // 处理 base64 图片
    if (data.image) {
      const imageBlob = base64Image2Blob(data.image, 'image/png');
      const imageSrc = URL.createObjectURL(imageBlob);
      chatStore.addMessage(createMessage({
        role: 'assistant',
        content: [
          { type: 'text', text: "这是根据您的要求生成的图表" } as MultimodalContent,
          { type: 'image_url', image_url: { url: imageSrc } } as MultimodalContent
        ],
        date: new Date().toISOString(),
        id: nanoid(),
      } as ExtendedChatMessage));
    } else {
      chatStore.addMessage(createMessage({
        role: 'assistant',
        content: [{ type: 'text', text: responseMessageContent } as MultimodalContent],
        date: new Date().toISOString(),
        id: nanoid(),
      }));
    }
  } catch (error) {
    let errorMsg;
    if (error instanceof Error) {
      errorMsg = `Error occurred: ${error.message || "Unknown error"}`;
    } else {
      errorMsg = "An unknown error occurred";
    }

    chatStore.addMessage(createMessage({
      role: 'assistant',
      content: [{ type: 'text', text: errorMsg } as MultimodalContent],
      date: new Date().toISOString(),
      id: nanoid(),
    }));
  }
}
