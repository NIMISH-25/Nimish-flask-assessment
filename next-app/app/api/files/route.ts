import { NextResponse } from "next/server";
import type { FileItem } from "@/lib/types";

const MOCK_FILES: FileItem[] = [
  { id: 1, name: "research_paper.pdf", size: "2.3 MB", date: "2024-01-15", user_name: "Test User" },
  { id: 2, name: "data_analysis.csv", size: "1.1 MB", date: "2024-01-20", user_name: "Test User" },
  { id: 3, name: "presentation.pptx", size: "5.2 MB", date: "2024-02-01", user_name: "Test User" },
];

export async function GET() {
  return NextResponse.json(MOCK_FILES);
}
