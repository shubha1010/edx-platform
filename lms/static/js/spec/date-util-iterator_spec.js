define(['../date-util-iterator.js'], function(DateUtilIterator) {
    'use strict';

    describe('DateUtilIterator', function() {
        beforeEach(function() {
            setFixtures('<div class="test"></div>');
        });

        describe('stringHandler', function() {
            it('returns a complete string', function() {
                var localTimeString = 'RANDOM_STRING';
                var sidecarString = 'RANDOM_STRING_TWO';
                var answer = 'RANDOM_STRING_TWO RANDOM_STRING';
                expect(DateUtilIterator.stringHandler(localTimeString, sidecarString)).toEqual(answer);
            });
        });

        describe('localizedTime', function() {
            var context;
            it('returns an empty string if provided no time', function() {
                context = {}
                expect(DateUtilIterator.localizedTime(context)).toEqual('');
            });
            it('returns a timezone formatted string', function() {
                var TestLangs = {
                    en: 'Oct 14, 2016 08:00 UTC',
                    ru: '14 окт. 2016 г. 08:00 UTC',
                    ar: '١٤ تشرين الأول أكتوبر ٢٠١٦ ٠٨:٠٠ UTC'
                };
                Object.keys(TestLangs).forEach(function(key) {
                    console.log(key)
                    var context = {
                        datetime: '2016-10-14 08:00:00+00:00',
                        timezone: 'UTC',
                        language: key
                    };
                    console.log(context)
                    expect(DateUtilIterator.localizedTime(context)).toEqual(TestLangs[key]);
                });
            });
        });
        describe('transform', function() {
           console.log('WORK HERE')
        });
        // transform
        // localizedTime: localizedTime,
        // stringHandler: stringHandler

        // describe('iterator', function() {
        // it('returns an empty string if provided no time', function() {
        //         expect(DateUtils.stringToMoment()).toEqual(undefined);
        //     });
        //     it('converts a string to a moment.js object', function() {
        //         expect(
        //             DateUtils.stringToMoment('2016-10-14 08:00:00+00:00').format('ll')
        //         ).toEqual('Oct 14, 2016');
        //     });
        // });
    });
});
