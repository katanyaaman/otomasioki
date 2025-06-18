import fs from 'fs/promises';
import path from 'path';

const TEMPLATE_PATH = path.resolve(__dirname, '../report/template/template.html');
const REPORT_DIR = path.resolve(__dirname, '../report/html');
const JSON_REPORT_DIR = path.resolve(__dirname, '../report/json');

export async function generateReport(testName: string, data: any[]) {
  try {
    // Pastikan direktori ada
    await fs.mkdir(REPORT_DIR, { recursive: true });
    await fs.mkdir(JSON_REPORT_DIR, { recursive: true });

    // Baca template HTML
    const template = await fs.readFile(TEMPLATE_PATH, 'utf-8');

    // Ubah data menjadi string JSON untuk disisipkan ke HTML
    const dataJsonString = JSON.stringify(data, null, 2);

    // Ganti placeholder di template dengan data JSON
    const finalHtml = template.replace(
      'var jsonData = {}; // Placeholder',
      `var jsonData = ${dataJsonString};`
    );

    const timestamp = new Date().toISOString().replace(/:/g, '-');
    const reportFileName = `${testName}-${timestamp}.html`;
    const jsonFileName = `${testName}-${timestamp}.json`;
    const reportFilePath = path.join(REPORT_DIR, reportFileName);
    const jsonFilePath = path.join(JSON_REPORT_DIR, jsonFileName);

    // Simpan file laporan HTML dan JSON
    await fs.writeFile(reportFilePath, finalHtml);
    await fs.writeFile(jsonFilePath, dataJsonString);

    console.log(`Laporan HTML berhasil dibuat di: ${reportFilePath}`);
    console.log(`Laporan JSON berhasil dibuat di: ${jsonFilePath}`);

  } catch (error) {
    console.error('Gagal membuat laporan:', error);
  }
}