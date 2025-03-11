export function formatDate(date: Date): string {
  return new Intl.DateTimeFormat("en-US", {
    dateStyle: "medium",
    timeStyle: "short",
  }).format(date);
}

// export function detectLanguage(content: string): string | undefined {
//   if (content.startsWith("<")) return "html";
//   if (content.includes("function")) return "javascript";
//   return undefined;
// }
