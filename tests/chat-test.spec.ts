import { test, expect, Page } from '@playwright/test';
import fs from 'fs';
import path from 'path';
import Papa from 'papaparse';
import { generateReport } from '../src/reportGenerator';
// import { getLlmScore } from '../src/llmService'; // Aktifkan jika diperlukan

// --- Konfigurasi Awal ---
const TEST_NAME = 'Test Knowledge Base';
const CSV_FILE_PATH = path.resolve(__dirname, '../assets/csv/kb_asuransi_10.csv');
const URL_TARGET = "https://www.brins.co.id/"; // Ganti dengan URL target Anda

// --- Fungsi Helper untuk Logika Tes ---

async function readCsv(filePath: string): Promise<any[]> {
  const csvFile = fs.readFileSync(filePath, 'utf8');
  return new Promise(resolve => {
    Papa.parse(csvFile, {
      header: true,
      skipEmptyLines: true,
      complete: (results) => {
        resolve(results.data);
      },
    });
  });
}

async function performChat(page: Page, question: string): Promise<string> {
  console.log(`Mengirim pertanyaan: ${question}`);

  // Klik tombol chat untuk membuka iframe
  await page.locator('xpath=//div[@class="brins-chat-icon"]').click();
  
  // Tunggu iframe muncul dan dapatkan framenya
  const chatIframe = page.frameLocator('xpath=//iframe[@id="brins-chat-iframe"]');
  
  // Interaksi di dalam iframe
  const questionInput = chatIframe.locator('xpath=//input[@placeholder="Tanya di sini..."]');
  await questionInput.fill(question);
  await questionInput.press('Enter');

  // Tunggu jawaban dari bot. Locator ini mungkin perlu disesuaikan.
  // Menunggu elemen jawaban terakhir muncul.
  await page.waitForTimeout(5000); // Tunggu statis 5 detik agar bot sempat merespon

  const lastBotResponse = await chatIframe.locator('xpath=//div[contains(@class, "bot-chat")]').last().innerText();
  console.log(`Menerima jawaban: ${lastBotResponse}`);
  
  // Tutup jendela chat
  await page.locator('xpath=//div[@class="brins-chat-icon"]').click();
  
  return lastBotResponse;
}

// --- Deskripsi Tes Utama ---

test.describe(TEST_NAME, () => {
  let testData: any[];

  // Sebelum semua tes berjalan, baca data dari CSV
  test.beforeAll(async () => {
    testData = await readCsv(CSV_FILE_PATH);
    expect(testData.length).toBeGreaterThan(0, 'Data CSV tidak boleh kosong');
  });

  // Iterasi dan jalankan tes untuk setiap baris data dari CSV
  for (let i = 0; i < testData.length; i++) {
    const row = testData[i];
    const question = row.question;
    const expectedAnswer = row.answer;

    test(`Test Case ${i + 1}: ${question}`, async ({ page }) => {
      const results = [];
      
      await page.goto(URL_TARGET, { waitUntil: 'networkidle' });

      const actualAnswer = await performChat(page, question);
      
      // (Opsional) Dapatkan skor dari LLM jika diperlukan
      // const llmScore = await getLlmScore(question, actualAnswer, expectedAnswer);
      
      const result = {
          'id': i + 1,
          'question': question,
          'expected_answer': expectedAnswer,
          'actual_answer': actualAnswer,
          // 'llm_score': llmScore,
          'status': actualAnswer.trim() !== '' ? 'Pass' : 'Fail' // Logika status sederhana
      };
      results.push(result);
      
      // Generate laporan untuk tes ini
      await generateReport(TEST_NAME, results);

      // Verifikasi dasar
      expect(actualAnswer).not.toBeNull();
      expect(actualAnswer.trim()).not.toEqual('');
    });
  }
});