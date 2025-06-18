import { defineConfig, devices } from '@playwright/test';
import dotenv from 'dotenv';
import path from 'path';

// Baca file .env jika ada
dotenv.config({ path: path.resolve(__dirname, '.env') });

export default defineConfig({
  testDir: './tests',
  /* Waktu maksimum untuk satu tes berjalan */
  timeout: 60 * 1000, // 60 detik
  expect: {
    timeout: 5000
  },
  /* Jalankan tes secara paralel */
  fullyParallel: true,
  /* Opsi untuk reporter */
  reporter: 'html',
  
  use: {
    /* Browser yang digunakan. Opsi: 'chromium', 'firefox', 'webkit' */
    browserName: 'chromium',
    
    /* Jalankan browser dalam mode headless (tanpa UI) secara default */
    headless: true,

    /* Ambil screenshot jika terjadi kegagalan */
    screenshot: 'only-on-failure',

    /* Ambil jejak eksekusi (trace) jika terjadi kegagalan. Sangat berguna! */
    trace: 'on-first-retry',
  },

  /* Konfigurasi spesifik untuk setiap proyek/browser */
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],
});