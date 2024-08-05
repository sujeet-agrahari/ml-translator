import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { TranslatorComponent } from './translator/translator.component';

const routes: Routes = [
  // { path: '', component: HomeComponent },
  { path: 'translator', component: TranslatorComponent },
  // other routes
];


@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
