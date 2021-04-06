describe('angular-material paginator component page', () => {
  const EC = protractor.ExpectedConditions;

  beforeAll(async() => {
    await browser.get('https://material.angular.io/components/paginator/examples');

    await browser.wait(EC.elementToBeClickable($('.mat-button-wrapper > .mat-icon')), 5000);
  });

  it('Should navigate to next page', async() => {
    await $('button[aria-label=\'Next page\']').click();
    
    await expect($('.mat-paginator-range-label').getAttribute('innerText')).toEqual('11 – 20 of 100');
  });

  it('Should navigate to previous page', async() => {
    await $('button[aria-label=\'Previous page\']').click();
    
    await expect($('.mat-paginator-range-label').getAttribute('innerText')).toEqual('1 – 10 of 100');
  });

  it('Should change list length to 5 items per page', async() => {
    await $('mat-select > div').click();
    
    const fiveItemsOption = $$('mat-option > .mat-option-text').first();

    await fiveItemsOption.click();
    
    await expect($('.mat-paginator-range-label').getAttribute('innerText')).toEqual('1 – 5 of 100');
  });
});
