import { TestBed, inject } from '@angular/core/testing';

import { MpatrolService } from './mpatrol.service';

describe('MpatrolService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [MpatrolService]
    });
  });

  it('should be created', inject([MpatrolService], (service: MpatrolService) => {
    expect(service).toBeTruthy();
  }));
});
