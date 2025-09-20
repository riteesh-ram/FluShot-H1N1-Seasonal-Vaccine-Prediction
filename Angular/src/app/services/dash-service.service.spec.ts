import { TestBed } from '@angular/core/testing';

import { DashServiceService } from './dash-service.service';

describe('DashServiceService', () => {
  let service: DashServiceService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(DashServiceService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
