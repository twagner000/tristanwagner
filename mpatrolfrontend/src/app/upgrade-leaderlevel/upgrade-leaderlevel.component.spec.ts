import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { UpgradeLeaderlevelComponent } from './upgrade-leaderlevel.component';

describe('UpgradeLeaderlevelComponent', () => {
  let component: UpgradeLeaderlevelComponent;
  let fixture: ComponentFixture<UpgradeLeaderlevelComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ UpgradeLeaderlevelComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(UpgradeLeaderlevelComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
