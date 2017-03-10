import { JamNgPage } from './app.po';

describe('jam-ng App', () => {
  let page: JamNgPage;

  beforeEach(() => {
    page = new JamNgPage();
  });

  it('should display message saying app works', () => {
    page.navigateTo();
    expect(page.getParagraphText()).toEqual('app works!');
  });
});
