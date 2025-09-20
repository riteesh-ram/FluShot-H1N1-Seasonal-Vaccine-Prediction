import { TestBed } from '@angular/core/testing';

import { RouteGuard2Guard } from './route-guard2.guard';

describe('RouteGuard2Guard', () => {
  let guard: RouteGuard2Guard;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    guard = TestBed.inject(RouteGuard2Guard);
  });

  it('should be created', () => {
    expect(guard).toBeTruthy();
  });
});
