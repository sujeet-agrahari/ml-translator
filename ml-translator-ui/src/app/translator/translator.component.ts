import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import jsPDF from 'jspdf';

@Component({
  selector: 'app-translator',
  templateUrl: './translator.component.html',
  styleUrls: ['./translator.component.scss']
})
export class TranslatorComponent {
  selectedFile: File | null = null;
  targetLanguage: string = 'hi_IN';
  downloadFilePath: string | null = null;
  languages = [
    { name: 'Arabic', code: 'ar_AR' },
    { name: 'Czech', code: 'cs_CZ' },
    { name: 'German', code: 'de_DE' },
    { name: 'English', code: 'en_XX' },
    { name: 'Spanish', code: 'es_XX' },
    { name: 'Estonian', code: 'et_EE' },
    { name: 'Finnish', code: 'fi_FI' },
    { name: 'French', code: 'fr_XX' },
    { name: 'Gujarati', code: 'gu_IN' },
    { name: 'Hindi', code: 'hi_IN' },
    { name: 'Italian', code: 'it_IT' },
    { name: 'Japanese', code: 'ja_XX' },
    { name: 'Kazakh', code: 'kk_KZ' },
    { name: 'Korean', code: 'ko_KR' },
    { name: 'Lithuanian', code: 'lt_LT' },
    { name: 'Latvian', code: 'lv_LV' },
    { name: 'Burmese', code: 'my_MM' },
    { name: 'Nepali', code: 'ne_NP' },
    { name: 'Dutch', code: 'nl_XX' },
    { name: 'Romanian', code: 'ro_RO' },
    { name: 'Russian', code: 'ru_RU' },
    { name: 'Sinhala', code: 'si_LK' },
    { name: 'Turkish', code: 'tr_TR' },
    { name: 'Vietnamese', code: 'vi_VN' },
    { name: 'Chinese', code: 'zh_CN' },
    { name: 'Afrikaans', code: 'af_ZA' },
    { name: 'Azerbaijani', code: 'az_AZ' },
    { name: 'Bengali', code: 'bn_IN' },
    { name: 'Persian', code: 'fa_IR' },
    { name: 'Hebrew', code: 'he_IL' },
    { name: 'Croatian', code: 'hr_HR' },
    { name: 'Indonesian', code: 'id_ID' },
    { name: 'Georgian', code: 'ka_GE' },
    { name: 'Khmer', code: 'km_KH' },
    { name: 'Macedonian', code: 'mk_MK' },
    { name: 'Malayalam', code: 'ml_IN' },
    { name: 'Mongolian', code: 'mn_MN' },
    { name: 'Marathi', code: 'mr_IN' },
    { name: 'Polish', code: 'pl_PL' },
    { name: 'Pashto', code: 'ps_AF' },
    { name: 'Portuguese', code: 'pt_XX' },
    { name: 'Swedish', code: 'sv_SE' },
    { name: 'Swahili', code: 'sw_KE' },
    { name: 'Tamil', code: 'ta_IN' },
    { name: 'Telugu', code: 'te_IN' },
    { name: 'Thai', code: 'th_TH' },
    { name: 'Tagalog', code: 'tl_XX' },
    { name: 'Ukrainian', code: 'uk_UA' },
    { name: 'Urdu', code: 'ur_PK' },
    { name: 'Xhosa', code: 'xh_ZA' },
    { name: 'Galician', code: 'gl_ES' },
    { name: 'Slovene', code: 'sl_SI' }
  ];
  constructor(private http: HttpClient) { }

  onFileSelected(event: any): void {
    this.selectedFile = event.target.files[0];
  }

  translate(): void {

    if (this.selectedFile && this.targetLanguage) {
      this.downloadFilePath = 'downloads/translated_output.pdf';
      const payload = {
        'input_text': 'Hello. how are you?',
        'target_language': this.targetLanguage
      }
      // const formData = new FormData();
      // formData.append('input_text', 'Hello. how are you?')
      // // formData.append('file', this.selectedFile);
      // formData.append('target_language', this.targetLanguage);

      this.http.post('http://localhost:3000/translate', payload,  { responseType: 'text' })
        .subscribe(
          response => {
            console.log("response", response);
             // Generate PDF
             const doc = new jsPDF();
             doc.text(response, 10, 10);
             
             // Save the PDF
             doc.save('translated_output.pdf');
            
          },
          error => {
            console.error('Translation error:', error);
          }
        );
    } else {
      alert('Please select a file and a target language.');
    }
  }
}
